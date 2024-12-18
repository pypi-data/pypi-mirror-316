from pydantic import Field, ConfigDict
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import logging
from moapy.auto_convert import auto_schema, MBaseModel
from moapy.mdreporter import ReportUtil
from moapy.data_post import ResultMD, print_result_data
from moapy.wgsd.wgsd_oapi import generate_defaultinfo_markdown_report, get_markdownimg_base64
import matplotlib
matplotlib.use("TkAgg")  # 또는 "Qt5Agg", "MacOSX" 등 GUI 기반 backend
import base64

class WaveParamInput(MBaseModel):
    # Default wave parameters
    h_wave_height: float = Field(default=15, title="Wave Height (m)", description="The vertical distance between the wave crest and trough, representing the wave's height.")
    p_period: float = Field(default=12.16, title="Wave Period (s)", description="The time taken for two successive wave crests to pass a fixed point, indicating the wave's period.")
    h_water_depth: float = Field(default=50, title="Water Depth (m)", description="The vertical distance from the seabed to the water surface, representing the water's depth.")
    d_piledia: float = Field(default=1, title="Pile Diameter (m)", description="The diameter of the pile structure interacting with the wave forces.")
    model_config = ConfigDict(
        title="Wave Force Input Data",
        description="Wave Force Input Data"
    )

class CoefficientInput(MBaseModel):
    # Coefficients
    dragcoeff: float = Field(default=1.0, title="Drag Coefficient", description="A dimensionless number representing the drag resistance exerted by the fluid on the structure.")
    inertiacoeff: float = Field(default=2.0, title="Inertia Coefficient", description="A dimensionless number quantifying the inertia forces acting on the structure due to fluid acceleration.")
    model_config = ConfigDict(
        title="Coefficients",
        description="Wave Force Input Data"
    )

class PeriodInput(MBaseModel):
    result_period: float = Field(
        default=0,
        title="Time Interval for Calculate Wave Force", 
        description="The time interval (in seconds) for calculating wave loads. Adjust this value to control the wave period and compute corresponding loads.")

    model_config = ConfigDict(
        title="Coefficients",
        description="Wave Force Input Data"
    )

class InputData(MBaseModel):
    wave_param: WaveParamInput = Field(default_factory=WaveParamInput, title="Wave Parameters Inputs")
    coeff: CoefficientInput = Field(default_factory=CoefficientInput, title="Coefficients Inputs")
    period: PeriodInput = Field(default_factory=PeriodInput, title="Define Time Step")
    model_config = ConfigDict(
        title="",
    )

class WaveForceCalculator:
    def __init__(self, input_data: InputData):
        # Constants
        self.g = 9.80665  # Gravity (m/s^2)
        self.rho = 10.1  # Seawater density (kN/m^3)
        self.pi = math.pi
        # Slider initial time

        # Wave parameters from input data
        wave_param = input_data.wave_param
        self.H = wave_param.h_wave_height
        self.T = wave_param.p_period
        self.h = wave_param.h_water_depth
        self.D = wave_param.d_piledia
        # Coefficients
        coeff = input_data.coeff
        self.Cd = coeff.dragcoeff
        self.Cm = coeff.inertiacoeff
        
        period = input_data.period
        self.result_period = period.result_period
        self.kc = None   # Keulegan-Carpenter number (calculated)
        
        # Calculate wavelength and wave number
        self.L = self.calculate_wavelength()[1]
        self.k = 2 * self.pi / self.L
        self.omega = 2 * self.pi / self.T
        self.initial_time =period.result_period
    def calculate_wavelength(self):
        """Calculate wavelength using dispersion relationship"""
        L0 = (self.g * self.T**2) / (2 * self.pi)  # Deep water wavelength
        L = L0  # Initial guess
        
        for _ in range(100):  # Iterative solution
            L_new = L0 * np.tanh(2 * self.pi * self.h / L)
            if abs(L - L_new) < 0.001:
                break
            L = L_new
        return L0, L  # Return both deep water wavelength and actual wavelength

    def calculate_wave_elevation(self, x, t):
        """Calculate wave surface elevation η at position x and time t."""
        phase_shift = -self.k + self.pi/2
        eta = (self.H / 2) * np.sin(self.k * x - self.omega * t + phase_shift)
        return eta

    def calculate_dynamic_depths(self, t, x):
        """
        Calculate dynamic depths based on current wave surface elevation at the given x position.
        """
        # Calculate instantaneous water surface elevation at x
        eta = self.calculate_wave_elevation(x, t)
        
        # Create depths from seabed to eta with consistent intervals
        num_points = 50  # Adjust as needed for resolution
        depths = np.linspace(-self.h, eta, num_points)
        
        return depths

    def calculate_wave_kinematics(self, z, t, x):
        """Calculate wave kinematics using linear wave theory at position x."""
        # Wave velocity and acceleration components
        k = self.k
        omega = self.omega
        u = (self.pi * self.H / self.T) * \
            (np.cosh(k * (z + self.h)) / np.sinh(k * self.h)) * \
            np.cos(k * x - omega * t)
        
        du_dt = (2 * self.pi**2 * self.H / self.T**2) * \
                (np.cosh(k * (z + self.h)) / np.sinh(k * self.h)) * \
                np.sin(k * x - omega * t)

        return u, du_dt

    def calculate_force_components(self, z, t, x):
        """Calculate individual force components using Morison equation at position x."""
        u, du_dt = self.calculate_wave_kinematics(z, t, x)

        # Cross-sectional area
        A = self.pi * (self.D**2) / 4

        # Drag force (Inline component)
        Fd_inline = 0.5 * self.rho/self.g * self.Cd * self.D * abs(u) * u

        # Inertia force
        Fi = self.Cm * self.rho/self.g * A * du_dt

        # Total force (sum of inertia and drag forces)
        F_total = Fi + Fd_inline
        print(x,z,u, Fd_inline, Fi)
        return Fi, Fd_inline, F_total

    def calculate_force(self, z, t, x):
        """Calculate total wave force using Morison equation at position x."""
        Fi, Fd_inline, F_total = self.calculate_force_components(z, t, x)
        return F_total

    def calculate_velocity(self, z, t, x):
        """Calculate wave velocity at position x using linear wave theory."""
        u, _ = self.calculate_wave_kinematics(z, t, x)
        return u


def animate_wave_forces(calculator):
    """
    Create interactive plot for wave forces on pile with dynamic depths controlled by a slider.
    """
    fig, ax1 = plt.subplots(figsize=(14, 8))
    plt.subplots_adjust(bottom=0.25)  # Adjust bottom to make space for slider
    
    # Calculate wavelength and other parameters
    L = calculator.L
    k = calculator.k
    omega = calculator.omega
    
    # Set up primary axis (for wave profile)
    ax1.set_ylim(-calculator.h - 0.5, calculator.H + 0.5)
    ax1.set_xlabel('Distance (m)')
    ax1.set_ylabel('Water Level (m)')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='blue', linestyle='--', alpha=0.3)
    ax1.axhline(y=-calculator.h, color='brown', linestyle='-', alpha=0.3)
    
    # Set up secondary axis (for forces)
    ax2 = ax1.twiny()
    ax2.set_ylim(-calculator.h - 0.5, calculator.H + 0.5)
    ax2.set_xlabel('Force (kN/m)')
    
    # Add parameter textbox
    param_text = (
        f"Wave Parameters:\n"
        f"Period (T) = {calculator.T:.1f} s\n"
        f"Height (H) = {calculator.H:.2f} m\n"
        f"Depth (h) = {calculator.h:.1f} m\n"
        f"Length (L) = {L:.1f} m\n"
        f"Pile D = {calculator.D:.2f} m"
    )
    
    # Add textbox with parameters
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
    ax1.text(0.02, 0.98, param_text,
             transform=ax1.transAxes,
             fontsize=9,
             verticalalignment='top',
             bbox=props)
    
    # Set up wave profile points
    x_points = np.linspace(-L/2, L*1.5, 200)
    ax1.set_xlim(-L/2, L*1.5)
    
    # Initialize plots
    wave_line, = ax1.plot([], [], 'b-', lw=2, label='Wave Surface')
    
    # Placeholder for dynamic depth bars
    bars = []
    value_texts = []
    force_values = []  # Store force values for tooltips
    
    # Add pile at the center
    pile_x = L / 2  # Pile located at the center of the plot
    pile_width = calculator.D
    pile_rect = plt.Rectangle((pile_x - pile_width/2, -calculator.h), 
                              pile_width, calculator.h + calculator.H,
                              color='brown', alpha=0.5)
    ax1.add_patch(pile_rect)
    
    # Add vertical line at pile center
    ax1.axvline(x=pile_x, color='brown', linestyle='--', alpha=0.3)

    # Slider axis
    ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])  # [left, bottom, width, height]

    # Create the slider
    time_slider = Slider(
        ax=ax_slider,
        label='Time',
        valmin=0,
        valmax=calculator.T,
        valinit=calculator.initial_time,  # Use the initial_time from calculator
        valfmt='%1.2f s'
    )

    # Create an annotation for the tooltip
    tooltip = ax2.annotate(
        '',
        xy=(0, 0),
        xytext=(20, 20),
        textcoords='offset points',
        bbox=dict(boxstyle='round', fc='yellow', alpha=0.7),
        arrowprops=dict(arrowstyle='->')
    )
    tooltip.set_visible(False)

    # Add dynamic text to show t/T
    time_text = ax1.text(0.8, 0.95, '', transform=ax1.transAxes, fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
    global_max_force = 0.0

    def update(val):
        nonlocal bars, value_texts, force_values, global_max_force
        t = time_slider.val - calculator.T / 2  # Center wave crest at x=0, t=0

        # Update time_text to show t/T
        time_fraction = t / calculator.T
        # time_text.set_text(f't/T = {time_fraction:.3f}')

        # Clear previous collections to prevent overlapping
        for collection in ax1.collections[:]:
            collection.remove()

        # Update wave profile
        eta_wave = [calculator.calculate_wave_elevation(x, t) for x in x_points]
        wave_line.set_data(x_points, eta_wave)

        # Calculate instantaneous η at pile position
        eta_at_pile = calculator.calculate_wave_elevation(pile_x, t)

        # Logging η at pile position
        logging.debug(f"Time: {t:.2f} s, Calculated η at pile: {eta_at_pile:.4f} m")

        # Calculate dynamic depths at current time and pile position
        depths = calculator.calculate_dynamic_depths(t, pile_x)

        # Remove previous bars and texts
        for bar in bars:
            bar.remove()
        for text in value_texts:
            text.remove()

        # Reinitialize bars and texts for current depths
        if len(depths) > 1:
            bar_height = depths[1] - depths[0]
        else:
            bar_height = 0.1  # Default height if only one depth
        bars_container = ax2.barh(depths, np.zeros_like(depths), height=bar_height, color='blue', alpha=0.7)
        bars = bars_container.patches
        value_texts = [ax2.text(0, y, '', ha='center', va='center', fontsize=8) for y in depths]

        # Calculate forces at each depth
        force_values = []
        table_data = []  # Table to store results
        for depth in depths:
            total_force = calculator.calculate_force(depth, t, pile_x)
            velocity = calculator.calculate_velocity(depth, t, pile_x)  # Calculate velocity at each depth
            force_values.append(total_force)  # Convert to kN/m
            # Append both force and velocity to the table data
            table_data.insert(0, {"depth": depth, "force": total_force, "velocity": velocity})
            global_max_force = max(global_max_force, abs(total_force))  # Update global max force

        # Update force bars and texts
        for bar, force, text in zip(bars, force_values, value_texts):
            bar.set_width(force)
            if abs(force) > 0.01:
                text.set_text(f'{force:.2f}')
                text.set_x(force + 0.1 if force > 0 else force - 0.1)
                bar.set_color('red' if force > 0 else 'blue')
            else:
                text.set_text('')
                bar.set_color('gray')
        ax2.set_xlim(-global_max_force * 1.3, global_max_force * 1.3)
        # Update water region
        ax1.fill_between(x_points, -calculator.h, eta_wave, color='lightblue', alpha=0.3)

        fig.canvas.draw_idle()
        print({"time": t, "table": table_data})
        return table_data
       
    # Define the on_hover function
    def on_hover(event):
        if event.inaxes == ax2:
            for bar, force in zip(bars, force_values):
                contains, _ = bar.contains(event)
                if contains:
                    z_pos = bar.get_y() + bar.get_height() / 2
                    tooltip.xy = (bar.get_width(), z_pos)
                    tooltip.set_text(f'z = {z_pos:.2f} m\nForce = {force:.2f} kN/m')
                    tooltip.set_visible(True)
                    fig.canvas.draw_idle()
                    return
            tooltip.set_visible(False)
            fig.canvas.draw_idle()
        else:
            tooltip.set_visible(False)
            fig.canvas.draw_idle()

    # Connect the slider and hover event
    time_slider.on_changed(update)
    fig.canvas.mpl_connect('motion_notify_event', on_hover)

    # Initialize the plot
    update(0)
    table_data = update(0)
    plt.title('Wave Forces on Pile')
    ax1.legend(['Water Surface'])
    plt.tight_layout()
    # plt.show()
    rpt = ReportUtil("test.md", "Wave Force Calculate Result")

    rpt.add_line('<h3 style="color: #343A3F; font-family: Arial, sans-serif;">Morrison Equation</h3>')
    rpt.add_line("")
    rpt.add_line('<div style="margin-top: 4px;">&nbsp;</div>')
    rpt.add_line("<br>")
    rpt.add_line('<p style="font-size: 18px; color: #343A3F; font-weight: 600; font-family: Arial, sans-serif; line-height: 1.5;">'
                '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                'F = ½ × Cᴅ × ρ₀ × D × U |U| + Cₘ × ρ₀ × πD²/4 × dU/dt</p>')

    rpt.add_line("<br>")
    rpt.add_line('<p style="font-size: 14px; font-weight: bold;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;>&nbsp;Where:</p>')
    rpt.add_line('<ul style="font-size: 6px; color: #343A3F; line-height: 0.8;">'
                '<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;F is the total wave force on the pile</li>'
                '<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;U is the wave velocity at depth</li>'
                '<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dU/dt is the wave acceleration</li>'
                f'<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Wave Height (H)&nbsp;: {calculator.H:.2f} m</li>'
                f'<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Wave Period (T)&nbsp;: {calculator.T:.2f} s</li>'
                f'<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Water Depth (h)&nbsp;: {calculator.h:.2f} m</li>'
                f'<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Pile Diameter (D)&nbsp;: {calculator.D:.2f} m</li>'
                f'<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Wave Length (L)&nbsp;: {calculator.L:.2f} m</li>'
                f'<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Density of sea water (ρ₀)&nbsp;: {calculator.rho:.2f} kN/m³</li>'
                f'<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Gravity (g)&nbsp;: {calculator.g:.4f} m/s²</li>'
                f'<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Drag Coefficient (Cᴅ)&nbsp;: {calculator.Cd:.2f}</li>'
                f'<li>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Inertia Coefficient (Cₘ)&nbsp;: {calculator.Cm:.2f}</li>'
                '</ul>')
    rpt.add_line("<br><br>\n")
    rpt.add_line('<h3 style="color: #343A3F; font-family: Arial, sans-serif;">Result Figure</h3>')
    rpt.add_line("<br>\n")
    # rpt.add_paragraph("Result Figure<br><br>\n")  # Markdown 헤더 형식 추가
    markdown_img = get_markdownimg_base64(0.9)
    rpt.add_line(markdown_img + "<br><br>\n")
    rpt.add_line('<h3 style="color: #343A3F; font-family: Arial, sans-serif;">Result Table</h3>')
    table_header = "\n| Depth (m) | Force (kN/m) | Velocity (m/s) |\n|-----------|--------------|----------------|\n"
    table_rows = "\n".join([f"| {row['depth']:.2f} | {row['force']:.2f} | {row['velocity']:.2f} |" for row in table_data])

    markdown_table_force = table_header + table_rows
    rpt.add_line("\n" + markdown_table_force)

    return ResultMD(md=rpt.get_md_text())


@auto_schema(title="Linear Wave Force Analysis", description="Calculate wave forces on cylindrical structures. This function calculates the wave kinematics and resulting forces using linear wave theory and Morison's equation. It returns a visual representation of the forces and a detailed table of maximum force values.")
def calculator_wave_force(input1: InputData) -> ResultMD:
    # Create instances of InputData2 and InputData3
    calculator = WaveForceCalculator(input1)
    # Create interactive plot with slider and tooltips
    result_md = animate_wave_forces(calculator)

    return result_md


if __name__ == "__main__":
    res = calculator_wave_force(InputData())
    result_md = print_result_data(res)
    with open("resultmd_output.md", "w") as file:
        file.write(result_md)
    


