component_list = [
    {
        'id': 'G19_COMP_1',
        'standard': 'EN1992-1-1',
        'reference': ['4.2(Table 4.1)'],
        'title': 'Classification of exposure classes based on environmental conditions',
        'description': r"Exposure classes define the environmental conditions that influence the durability of concrete structures. These classes range from environments with no corrosion risk (X0) to those with risks of carbonation (XC), chloride ingress (XD), or marine exposure (XS). They guide the selection of materials and design measures to ensure long-term performance.",
        'latex_symbol': r'expoclass',
        'type': 'string',
        'unit': '',
        'notation': 'text',
        'default': 'X0 (No risk of corrosion or attack)',
        'table': 'dropdown',
    },
    {
        'id': 'G19_COMP_2',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.3(4)'],
        'title': 'Concrete casting conditions',
        'description': r"The Concrete Casting Conditions table outlines three scenarios: the general case, where standard deviation is considered; prepared ground, which requires additional cover for flat surfaces like blinding layers; and direct soil casting, where a larger cover is needed due to the irregularity of the soil.",
        'latex_symbol': r'castcond',
        'type': 'string',
        'unit': '',
        'notation': 'text',
        'default': 'General case',
        'table': 'dropdown',
    },
    {
        'id': 'G19_COMP_3',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.1(4.1)'],
        'title': 'Nominal cover for concrete under various conditions',
        'description': r"The nominal cover for concrete refers to the total distance between the surface of the reinforcement and the outer surface of the concrete. It is determined by adding the minimum cover, which ensures durability and protection against corrosion, along with an allowance for potential deviations during construction.",
        'latex_symbol': r'c_{nom}',
        'latex_equation': r'c_{nom} = c_{min} + \Delta{c_{dev}}',
        'type': 'number',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 3,
        'required': ['G19_COMP_7', 'G19_COMP_6', 'G19_COMP_4', 'G19_COMP_5'],
        'table': 'formula',
    },
    {
        'id': 'G19_COMP_4',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.3(4)'],
        'title': 'Cover allowance for concrete cast on prepared ground',
        'description': r"When casting concrete on prepared ground, such as a blinding layer, the minimum additional cover thickness is typically set at 40mm. This is to account for surface unevenness and to ensure proper reinforcement protection. This cover thickness is commonly applied in cases like foundation slabs or footings on compacted gravel, where the surface is relatively flat.",
        'latex_symbol': r'k_{1}',
        'type': 'number',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 1,
        'required': ['G19_COMP_2'],
        'default': 40.0,
        'const': True,
    },
    {
        'id': 'G19_COMP_5',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.3(4)'],
        'title': 'Cover allowance for concrete cast directly on soil',
        'description': r"When casting concrete directly on soil, a thicker cover is required due to the irregularity of the soil surface. The recommended minimum cover thickness is 75mm to ensure structural durability. This applies to situations such as culverts, retaining wall footings, or pipelines embedded directly in soil to protect the reinforcement and maintain long-term durability.",
        'latex_symbol': r'k_{2}',
        'type': 'number',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 1,
        'required': ['G19_COMP_2'],
        'default': 75.0,
        'const': True,
    },
    {
        'id': 'G19_COMP_6',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.3(1)P'],
        'title': 'Allowance for deviation in concrete cover',
        'description': r"This refers to the additional amount added to the minimum concrete cover to account for possible deviations that may occur during construction. The value of this allowance helps ensure that even with variations in workmanship, the concrete cover will still meet the required standards for durability and protection. The exact value of the allowance is typically specified in national standards or regulations.",
        'latex_symbol': r'\Delta{c_{dev}}',
        'type': 'number',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 1,
        'default': 10.0,
        'const': True,
    },
    {
        'id': 'G19_COMP_7',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(4.2)'],
        'title': 'Minimum concrete cover',
        'description': r"This is the minimum required distance between the outer surface of the reinforcement and the concrete surface. The minimum cover takes into account factors such as durability, bond, and potential environmental conditions.",
        'latex_symbol': r'c_{min}',
        'latex_equation': r'c_{min} = \max(c_{min,b}, c_{min,dur} + \Delta{c_{dur,\gamma}} - \Delta{c_{dur,st}} - \Delta{c_{dur,add}}, 10) + \Delta{c_{uneven}} + \Delta{c_{abrasion}}',
        'type': 'number',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 3,
        'required': ['G19_COMP_21', 'G19_COMP_30', 'G19_COMP_12', 'G19_COMP_13', 'G19_COMP_14', 'G19_COMP_9', 'G19_COMP_11'],
    },
    {
        'id': 'G19_COMP_8',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(11)'],
        'title': 'Select uneven surface type for minimum cover adjustment',
        'description': r"Choose the type of uneven surface to adjust the minimum cover requirement. Based on the surface condition (e.g., exposed aggregate or smooth surface), the cover thickness will be increased as per the specified values.",
        'latex_symbol': r'unsurtype',
        'type': 'string',
        'unit': 'mm',
        'notation': 'text',
        'default': 'Exposed Aggregate',
        'table': 'dropdown',
    },
    {
        'id': 'G19_COMP_9',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(11)'],
        'title': 'Increase in minimum cover for uneven surfaces',
        'description': r"For concrete cast against uneven surfaces, such as exposed aggregate finishes, the minimum cover must be increased by at least 5 mm. This is to ensure adequate protection of reinforcement in areas where surface irregularities could reduce the actual cover thickness.",
        'latex_symbol': r'\Delta{c_{uneven}}',
        'latex_equation': r'\Delta{c_{uneven}} = 5',
        'type': 'number',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 1,
        'required': ['G19_COMP_8'],
        'table': 'formula',
    },
    {
        'id': 'G19_COMP_10',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(13)'],
        'title': 'Select concrete abrasion class for cover',
        'description': r"Choose the appropriate abrasion class to adjust the concrete cover based on the expected wear and tear. This selection will affect the required concrete cover thickness depending on the abrasion conditions, such as moderate, heavy, or extreme abrasion.",
        'latex_symbol': r'abraclass',
        'type': 'string',
        'unit': '',
        'notation': 'text',
        'default': 'None',
        'table': 'dropdown',
    },
    {
        'id': 'G19_COMP_11',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(13)'],
        'title': 'Concrete abrasion class',
        'description': r"Abrasion Class XM1 refers to moderate abrasion, such as in industrial sites where vehicles with air tires are commonly used. Abrasion Class XM2 refers to heavy abrasion, typically found in industrial sites frequented by forklifts with air or solid rubber tires. Abrasion Class XM3 indicates extreme abrasion, like in industrial sites where forklifts with elastomer or steel tires, or track vehicles, are used.",
        'latex_symbol': r'\Delta{c_{abrasion}}',
        'latex_equation': r'\Delta{c_{abrasion}} = 0',
        'type': 'number',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 1,
        'required': ['G19_COMP_10'],
        'table': 'formula',
    },
    {
        'id': 'G19_COMP_12',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(6)'],
        'title': 'Safety factor for durability',
        'description': r"This value is an additional safety allowance added to the minimum cover for durability to account for uncertainties in environmental conditions, material properties, or other factors that might affect the structure's durability.",
        'latex_symbol': r'\Delta{c_{dur,\gamma}}',
        'type': 'number',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 1,
        'default': 0.0,
        'const': True,
    },
    {
        'id': 'G19_COMP_13',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(7)'],
        'title': 'Reduction of concrete cover due to durability enhancements',
        'description': r"This reduction applies when stainless steel or other special protective measures are used in the structure. These materials provide higher durability, allowing the concrete cover to be reduced while maintaining structural integrity. The reduction must account for the effects on all relevant material properties, including bond strength.",
        'latex_symbol': r'\Delta{c_{dur,st}}',
        'type': 'number',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 1,
        'default': 0.0,
        'const': True,
    },
    {
        'id': 'G19_COMP_14',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(8)'],
        'title': 'Additional cover for special exposure conditions',
        'description': r"This is the additional cover that may be required when the structure is exposed to particularly aggressive environmental conditions, such as harsh chemicals, extreme weather, or other factors that increase the risk of damage.",
        'latex_symbol': r'\Delta{c_{dur,add}}',
        'type': 'number',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 1,
        'default': 0.0,
        'const': True,
    },
    {
        'id': 'G19_COMP_15',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(Table4.2)'],
        'title': 'Arrangement of bars',
        'description': r"This table allows the selection of how the reinforcement bars are arranged in the concrete structure. Bars can either be separated, where individual bars are spaced apart, or bundled, where multiple bars are grouped together. The arrangement affects the concrete cover, bonding, and overall strength of the structure.",
        'latex_symbol': r'bararrange',
        'type': 'string',
        'unit': '',
        'notation': 'text',
        'default': 'Separated',
        'table': 'dropdown',
    },
    {
        'id': 'G19_COMP_16',
        'standard': 'EN1992-1-1',
        'reference': ['7.3.3 (Table7.2N)'],
        'title': 'Maximum diameter of reinforcement',
        'description': r"This refers to the maximum diameter of the reinforcing steel bars used in the concrete structure. It is a critical parameter in determining the necessary concrete cover to ensure proper bonding and protection against environmental factors. The diameter is selected based on design requirements and structural loads.",
        'latex_symbol': r'\phi',
        'type': 'string',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 0,
        'default': '8',
        'table': 'dropdown',
    },
    {
        'id': 'G19_COMP_17',
        'standard': 'EN1992-1-1',
        'reference': ['8.9.1(2)'],
        'title': 'Number of bars in a bundle',
        'description': r"This refers to the total number of reinforcement bars grouped together in a bundle. The number of bars in a bundle is allowed to range from a minimum of 2 to a maximum of 4, depending on the specific application.",
        'latex_symbol': r'n_{b}',
        'type': 'string',
        'unit': 'ea',
        'notation': 'standard',
        'decimal': 0,
        'default': '2',
        'table': 'dropdown',
    },
    {
        'id': 'G19_COMP_18',
        'standard': 'EN1992-1-1',
        'reference': ['8.9.1(8.14)'],
        'title': 'Equivalent diameter of a notional bar',
        'description': r"This is the equivalent diameter of a notional bar that replaces a bundle of bars in the design process. The notional bar has the same sectional area and center of gravity as the bundle. The equivalent diameter is calculated by taking the diameter of an individual bar in the bundle and multiplying it by the square root of the number of bars in the bundle. The maximum allowable equivalent diameter is 55 mm.",
        'latex_symbol': r'\phi_{n}',
        'latex_equation': r'\phi_{n} = \min(\phi \times \sqrt{n_{b}} , 55)',
        'type': 'number',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 3,
        'required': ['G19_COMP_16', 'G19_COMP_17'],
    },
    {
        'id': 'G19_COMP_19',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(Table4.2)'],
        'title': 'Select aggregate size for minimum cover',
        'description': r"Choose the aggregate size to adjust the minimum concrete cover for bond. Larger aggregate sizes may require an increase in the cover thickness to ensure proper bonding.",
        'latex_symbol': r'maxaggre',
        'type': 'string',
        'unit': '',
        'notation': 'text',
        'default': 'exceeds 32 mm',
        'table': 'dropdown',
    },
    {
        'id': 'G19_COMP_20',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(Table4.2)'],
        'title': 'Adjustment of minimum cover for bond based on aggregate size',
        'description': r"If the nominal maximum aggregate size used in the concrete mix exceeds 32 mm, the minimum concrete cover for bond should be increased by 5 mm. This adjustment ensures adequate bonding and protection of the reinforcement when larger aggregates are used in the mix.",
        'latex_symbol': r'aggresize',
        'latex_equation': r'aggresize = 5',
        'type': 'number',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 1,
        'required': ['G19_COMP_19'],
        'table': 'formula',
    },
    {
        'id': 'G19_COMP_21',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(3)'],
        'title': 'Minimum cover for bond',
        'description': r"This is the minimum concrete cover required to ensure adequate bond between the reinforcement and the concrete. It ensures that the reinforcement remains properly anchored and that the structural integrity is maintained.",
        'latex_symbol': r'c_{min,b}',
        'latex_equation': r'c_{min,b} = \phi + aggresize',
        'type': 'number',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 3,
        'required': ['G19_COMP_16', 'G19_COMP_18', 'G19_COMP_20', 'G19_COMP_15'],
        'table': 'formula',
    },
    {
        'id': 'G19_COMP_22',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(Table4.3N)'],
        'title': 'Structural class',
        'description': r"Structural Class refers to the classification system used to define the durability and performance requirements of a concrete structure. It takes into account factors like environmental exposure, design working life, and the required concrete strength to ensure long-term stability and resistance to deterioration. The structural class helps determine the necessary concrete cover and material specifications for different conditions.",
        'latex_symbol': r'S',
        'latex_equation': r'S = 4 + strucclass + strenclass + slabgeo + specqual',
        'type': 'number',
        'unit': '',
        'notation': 'standard',
        'decimal': 0,
        'required': ['G19_COMP_24', 'G19_COMP_25', 'G19_COMP_27', 'G19_COMP_29'],
    },
    {
        'id': 'G19_COMP_23',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(Table4.3N)'],
        'title': 'Select design working life for structural class',
        'description': r"Choose the design working life of the structure to adjust the structural class. Structures with a design life of 100 years or more require additional adjustments to ensure long-term durability.",
        'latex_symbol': r'wolife',
        'type': 'string',
        'unit': '',
        'notation': 'text',
        'default': 'less than 100 years',
        'table': 'dropdown',
    },
    {
        'id': 'G19_COMP_24',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(Table4.3N)'],
        'title': 'Adjustment of structural class based on Design working life',
        'description': r"This criterion determines whether the structure is designed for a 100-year lifespan. A longer design working life, such as 100 years, typically requires higher durability standards due to the extended exposure to environmental conditions and potential deterioration over time. As a result, a higher structural class may be required to ensure the structure's longevity and resistance to factors like corrosion, carbonation, or freeze-thaw cycles.",
        'latex_symbol': r'strucclass',
        'latex_equation': r'strucclass = 0',
        'type': 'number',
        'unit': '',
        'notation': 'standard',
        'decimal': 0,
        'required': ['G19_COMP_23'],
        'table': 'formula',
    },
    {
        'id': 'G19_COMP_25',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(Table4.3N)'],
        'title': 'Adjustment of structural class based on strength class',
        'description': r"The structural class may be adjusted according to the strength class of the concrete. Higher strength classes allow for improved durability, potentially lowering the required structural class by providing greater resistance to environmental factors and mechanical stresses.",
        'latex_symbol': r'strenclass',
        'latex_equation': r'strenclass = -1',
        'type': 'number',
        'unit': '',
        'notation': 'standard',
        'decimal': 0,
        'required': ['G19_COMP_1', 'G14_COMP_5'],
        'table': 'formula',
    },
    {
        'id': 'G19_COMP_26',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(Table4.3N)'],
        'title': 'Select slab option for structural class',
        'description': r'Choose the appropriate slab option to adjust the structural class based on the geometry. Selecting "Slab Geometry" will reduce the structural class by 1, while "Non-Slab Geometry" will have no effect on the structural class.',
        'latex_symbol': r'slabop',
        'type': 'string',
        'unit': '',
        'notation': 'text',
        'default': 'Slab Geometry',
        'table': 'dropdown',
    },
    {
        'id': 'G19_COMP_27',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(Table4.3N)'],
        'title': 'Adjustment of structural class based on slab geometry',
        'description': r"This criterion applies to structural members with slab geometry, where the position of reinforcement remains stable and is not significantly affected by construction activities. In such cases, the structural class can often be lower because the risks of reinforcement misplacement or improper concrete cover are minimized. The slab's uniformity allows for better quality control and reduced variability in the final structure.",
        'latex_symbol': r'slabgeo',
        'latex_equation': r'slabgeo = -1',
        'type': 'number',
        'unit': '',
        'notation': 'standard',
        'decimal': 0,
        'required': ['G19_COMP_26'],
        'table': 'formula',
    },
    {
        'id': 'G19_COMP_28',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(Table4.3N)'],
        'title': 'Select quality control option for structural class',
        'description': r'Choose the appropriate quality control option to adjust the structural class. Selecting "Special quality control ensured" will reduce the structural class by 1, while "Standard quality control" will maintain the current structural class without adjustments.',
        'latex_symbol': r'qualcon',
        'type': 'string',
        'unit': '',
        'notation': 'text',
        'default': 'Special quality control ensured',
        'table': 'dropdown',
    },
    {
        'id': 'G19_COMP_29',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(Table4.3N)'],
        'title': 'Adjustment of structural class based on special quality control',
        'description': r"This criterion applies to structural members with slab geometry, where the position of reinforcement remains stable and is not significantly affected by construction activities. In such cases, the structural class can often be lower because the risks of reinforcement misplacement or improper concrete cover are minimized. The slab's uniformity allows for better quality control and reduced variability in the final structure.",
        'latex_symbol': r'specqual',
        'latex_equation': r'specqual = -1',
        'type': 'number',
        'unit': '',
        'notation': 'standard',
        'decimal': 0,
        'required': ['G19_COMP_28'],
        'table': 'formula',
    },
    {
        'id': 'G19_COMP_30',
        'standard': 'EN1992-1-1',
        'reference': ['4.4.1.2(Table4.4N)'],
        'title': 'Minimum cover for durability',
        'description': r"This refers to the minimum concrete cover needed to protect the reinforcement from environmental exposure conditions such as corrosion, carbonation, or chloride-induced degradation. It helps ensure the long-term durability of the structure.",
        'latex_symbol': r'c_{min,dur}',
        'type': 'number',
        'unit': 'mm',
        'notation': 'standard',
        'decimal': 0,
        'required': ['G19_COMP_22', 'G19_COMP_1'],
        'table': 'formula',
    },
]
data_table = [
    {
        'id': 'G19_COMP_1',
        'enum': [
            {
                'label': 'X0 (No risk of corrosion or attack)',
                'description': 'This class applies to concrete without reinforcement or embedded metal, in all exposures where there is no risk of freeze/thaw cycles, abrasion, or chemical attack. The X0 class is for situations where no corrosion or degradation of metal materials is expected due to the absence of moisture or aggressive environments.',
                'Situations': 'Concrete inside buildings with very low air humidity, such as in heated or well-ventilated indoor spaces. For instance, concrete used in office buildings, industrial facilities, or residential buildings where exposure to moisture or external weather conditions is minimal.',
                'Structures': '- Interior columns, walls, or floors of commercial or residential buildings\n- Foundations or walls in sheltered areas, such as parking garages or storage facilities',
            },
            {
                'label': 'XC1 (Dry or permanently wet)',
                'description': 'This class applies to environments where concrete is either always dry or permanently submerged in water, with no significant moisture variation.',
                'Situations': '- Concrete inside buildings with low air humidity, such as offices or residential spaces.\n- Concrete structures permanently submerged in water, like water tanks or underwater elements.',
                'Structures': '- Interior walls, floors, or columns of buildings in controlled low humidity conditions.\n- Underwater Foundations or water tanks.',
            },
            {
                'label': 'XC2 (Wet, rarely dry)',
                'description': 'Concrete is typically wet and rarely dries, being in long-term contact with water.',
                'Situations': '- Concrete surfaces subject to continuous contact with water, such as water storage areas.\n- Foundations or structures exposed to groundwater.',
                'Structures': '- Water reservoirs, tanks, or other storage structures.\n- Foundations and footings in areas with high groundwater levels.',
            },
            {
                'label': 'XC3 (Moderate humidity)',
                'description': 'Concrete is exposed to environments with moderate or high humidity but not subjected to direct rain exposure.',
                'Situations': '- Concrete inside buildings with moderate to high humidity, such as basements or garages.\n- External concrete surfaces that are protected from direct rain exposure.',
                'Structures': '- Parking garages, basements, or garages with moderate humidity.\n- Covered walkways or facades of buildings.',
            },
            {
                'label': 'XC4 (Cyclic wet and dry)',
                'description': 'Concrete experiences alternating cycles of wet and dry conditions but does not fit into the XC2 class (long-term water contact).',
                'Situations': '- Concrete surfaces exposed to intermittent water contact, such as exterior walls, facades, or bridges.\n- Structures subject to seasonal or periodic wetting and drying.',
                'Structures': '- Building facades, bridges, or outdoor platforms.\n- Coastal structures or parking decks exposed to periodic wet and dry conditions.',
            },
            {
                'label': 'XD1 (Moderate humidity, exposure to airborne chlorides)',
                'description': 'Concrete exposed to environments with moderate humidity where airborne chlorides are present, which can lead to corrosion of reinforcement.',
                'Situations': '- Concrete surfaces in coastal areas where chlorides from sea air are present.\n- Structures near roads treated with de-icing salts during winter.',
                'Structures': '- Concrete facades or walls exposed to airborne chlorides.\n- Building exteriors in coastal or highway-adjacent areas.',
            },
            {
                'label': 'XD2 (Wet, rarely dry, exposure to chlorides)',
                'description': 'Concrete in contact with water that contains chlorides, typically in industrial or swimming pool environments where concrete is wet most of the time and rarely dries.',
                'Situations': '- Swimming pools with chloride-containing water.\n- Industrial facilities where water with dissolved chlorides is present.',
                'Structures': '- Concrete surfaces in swimming pools.\n- Structural elements exposed to industrial waters containing chlorides, such as tanks or pipelines.',
            },
            {
                'label': 'XD3 (Cyclic wet and dry, exposure to chlorides)',
                'description': 'Concrete that experiences cycles of wet and dry conditions, and is exposed to chlorides, often from road salts or seawater spray.',
                'Situations': '- Bridge components exposed to spray from roads treated with de-icing salts.\n- Surfaces of roads, pavements, or parking decks where chlorides are present.',
                'Structures': '- Bridge piers and other components exposed to chloride spray.\n- Pavements, parking slabs, and other exposed flat concrete surfaces subject to wet/dry cycles and chloride exposure.',
            },
            {
                'label': 'XS1 (Exposed to airborne salt but not in direct contact with sea water)',
                'description': 'Concrete is exposed to airborne salt from the sea, but not in direct contact with seawater. Typically, this includes coastal areas where structures are near the sea but not submerged.',
                'Situations': '- Structures located near the coast that are exposed to sea air containing salts.\n- Buildings and infrastructure within a certain distance from the shoreline.',
                'Structures': '- Coastal buildings, piers, and bridges not directly in contact with seawater.\n- Infrastructure such as roads and retaining walls near the coastline.',
            },
            {
                'label': 'XS2 (Permanently submerged)',
                'description': 'Concrete that is permanently submerged in seawater, such as parts of marine structures that are constantly underwater.',
                'Situations': '- Marine structures that are submerged below the waterline, such as sea walls and offshore platforms.\n- Foundations or parts of structures that are always in contact with seawater.',
                'Structures': '- Submerged parts of marine structures like jetties, offshore platforms, and piers.\n- Underwater foundations of bridges and coastal structures.',
            },
            {
                'label': 'XS3 (Tidal, splash, and spray zones)',
                'description': 'Concrete is exposed to tidal action, splash, and spray zones where the structure may be alternately wet and dry due to tidal movements or splashing seawater.',
                'Situations': '- Marine structures exposed to wave splash or tides, such as the base of coastal structures.\n- Areas exposed to seawater spray during high tides or storms.',
                'Structures': '- Parts of marine structures like sea walls, jetties, or piers in tidal zones.\n- Coastal bridges and infrastructure exposed to tidal action and seawater spray.',
            },
        ],
    },
    {
        'id': 'G19_COMP_2',
        'enum': [
            {'label': 'General case'},
            {'label': 'Prepared ground'},
            {'label': 'Direct soil'},
        ],
    },
    {
        'id': 'G19_COMP_3',
        'criteria': [
            [
                r'castcond = General case',
                r'castcond = Prepared ground',
                r'castcond = Direct soil',
            ]
        ],
        'data': [
            r'c_{nom} = c_{min} + \Delta{c_{dev}}',
            r'c_{nom} = max(c_{min} + \Delta{c_{dev}} , k_{1})',
            r'c_{nom} = max(c_{min} + \Delta{c_{dev}} , k_{2})',
        ],
    },
    {
        'id': 'G19_COMP_8',
        'enum': [
            {'label': 'Exposed Aggregate'},
            {'label': 'None'},
        ],
    },
    {
        'id': 'G19_COMP_9',
        'criteria': [
            [
                r'unsurtype = Exposed Aggregate',
                r'unsurtype = None'
            ]
        ],
        'data': [
            r'\Delta{c_{uneven}} = 5',
            r'\Delta{c_{uneven}} = 0'
        ],
    },
    {
        'id': 'G19_COMP_10',
        'enum': [
            {'label': 'None'},
            {'label': 'XM1 (Moderate abrasion: vehicles with air tires)'},
            {'label': 'XM2 (Heavy abrasion: forklifts with air or rubber tires)'},
            {'label': 'XM3 (Extreme abrasion: forklifts with steel tires or track vehicles)'},
        ],
    },
    {
        'id': 'G19_COMP_11',
        'criteria': [
            [
                r'abraclass = None',
                r'abraclass = XM1 (Moderate abrasion: vehicles with air tires)',
                r'abraclass = XM2 (Heavy abrasion: forklifts with air or rubber tires)',
                r'abraclass = XM3 (Extreme abrasion: forklifts with steel tires or track vehicles)',
            ]
        ],
        'data': [
            r'\Delta{c_{abrasion}} = 0',
            r'\Delta{c_{abrasion}} = 5',
            r'\Delta{c_{abrasion}} = 10',
            r'\Delta{c_{abrasion}} = 15',
        ],
    },
    {
        'id': 'G19_COMP_15',
        'enum': [
            {'label': 'Separated'},
            {'label': 'Bundled'}
        ]
    },
    {
        'id': 'G19_COMP_16',
        'enum': [
            {'label': '8'},
            {'label': '10'},
            {'label': '12'},
            {'label': '16'},
            {'label': '20'},
            {'label': '25'},
            {'label': '32'},
            {'label': '40'},
        ],
    },
    {
        'id': 'G19_COMP_17',
        'enum': [
            {'label': '2'},
            {'label': '3'},
            {'label': '4'}
        ],
    },
    {
        'id': 'G19_COMP_19',
        'enum': [
            {'label': 'exceeds 32 mm'},
            {'label': 'does not exceed 32 mm'}
        ],
    },
    {
        'id': 'G19_COMP_20',
        'criteria': [
            [
                r'maxaggre = exceeds 32 mm',
                r'maxaggre = does not exceed 32 mm'
            ]
        ],
        'data': [
            r'aggresize = 5',
            r'aggresize = 0'
        ],
    },
    {
        'id': 'G19_COMP_21',
        'criteria': [
            [
                r'bararrange = Separated',
                r'bararrange = Bundled'
            ]
        ],
        'data': [
            r'c_{min,b} = \phi + aggresize',
            r'c_{min,b} = \phi_{n} + aggresize',
        ],
    },
    {
        'id': 'G19_COMP_23',
        'enum': [
            {'label': 'less than 100 years'},
            {'label': '100 years or more'}
        ],
    },
    {
        'id': 'G19_COMP_24',
        'criteria': [
            [
                r'wolife = less than 100 years',
                r'wolife = 100 years or more'
            ]
        ],
        'data': [
            r'strucclass = 0',
            r'strucclass = 2'
        ],
    },
    {
        'id': 'G19_COMP_25',
        'criteria': [
            [
                r'expoclass = X0 (No risk of corrosion or attack) \land f_{ck} >= 30',
                r'expoclass = X0 (No risk of corrosion or attack) \land f_{ck} < 30',
                r'expoclass = XC1 (Dry or permanently wet) \land f_{ck} >= 30',
                r'expoclass = XC1 (Dry or permanently wet) \land f_{ck} < 30',
                r'expoclass = XC2 (Wet, rarely dry) \land f_{ck} >= 35',
                r'expoclass = XC2 (Wet, rarely dry) \land f_{ck} < 35',
                r'expoclass = XC3 (Moderate humidity) \land f_{ck} >= 35',
                r'expoclass = XC3 (Moderate humidity) \land f_{ck} < 35',
                r'expoclass = XC4 (Cyclic wet and dry) \land f_{ck} >= 40',
                r'expoclass = XC4 (Cyclic wet and dry) \land f_{ck} < 40',
                r'expoclass = XD1 (Moderate humidity, exposure to airborne chlorides) \land f_{ck} >= 40',
                r'expoclass = XD1 (Moderate humidity, exposure to airborne chlorides) \land f_{ck} < 40',
                r'expoclass = XD2 (Wet, rarely dry, exposure to chlorides) \land f_{ck} >= 40',
                r'expoclass = XD2 (Wet, rarely dry, exposure to chlorides) \land f_{ck} < 40',
                r'expoclass = XD3 (Cyclic wet and dry, exposure to chlorides) \land f_{ck} >= 45',
                r'expoclass = XD3 (Cyclic wet and dry, exposure to chlorides) \land f_{ck} < 45',
                r'expoclass = XS1 (Exposed to airborne salt but not in direct contact with sea water) \land f_{ck} >= 40',
                r'expoclass = XS1 (Exposed to airborne salt but not in direct contact with sea water) \land f_{ck} < 40',
                r'expoclass = XS2 (Permanently submerged) \land f_{ck} >= 45',
                r'expoclass = XS2 (Permanently submerged) \land f_{ck} < 45',
                r'expoclass = XS3 (Tidal, splash, and spray zones) \land f_{ck} >= 45',
                r'expoclass = XS3 (Tidal, splash, and spray zones) \land f_{ck} < 45',
            ]
        ],
        'data': [
            r'strenclass = -1',
            r'strenclass = 0',
            r'strenclass = -1',
            r'strenclass = 0',
            r'strenclass = -1',
            r'strenclass = 0',
            r'strenclass = -1',
            r'strenclass = 0',
            r'strenclass = -1',
            r'strenclass = 0',
            r'strenclass = -1',
            r'strenclass = 0',
            r'strenclass = -1',
            r'strenclass = 0',
            r'strenclass = -1',
            r'strenclass = 0',
            r'strenclass = -1',
            r'strenclass = 0',
            r'strenclass = -1',
            r'strenclass = 0',
            r'strenclass = -1',
            r'strenclass = 0',
        ],
    },
    {
        'id': 'G19_COMP_26',
        'enum': [
            {'label': 'Slab Geometry'},
            {'label': 'Non-Slab Geometry'}
        ],
    },
    {
        'id': 'G19_COMP_27',
        'criteria': [
            [
                r'slabop = Slab Geometry',
                r'slabop = Non-Slab Geometry'
            ]
        ],
        'data': [
            r'slabgeo = -1',
            r'slabgeo = 0'
        ],
    },
    {
        'id': 'G19_COMP_28',
        'enum': [
            {'label': 'Special quality control ensured'},
            {'label': 'Standard quality control'},
        ],
    },
    {
        'id': 'G19_COMP_29',
        'criteria': [
            [
                r'qualcon = Special quality control ensured',
                r'qualcon = Standard quality control',
            ]
        ],
        'data': [
            r'specqual = -1',
            r'specqual = 0'
        ],
    },
    {
        'id': 'G19_COMP_30',
        'criteria': [
            [
                r'expoclass = X0 (No risk of corrosion or attack)',
                r'expoclass = XC1 (Dry or permanently wet)',
                r'expoclass = XC2 (Wet, rarely dry)',
                r'expoclass = XC3 (Moderate humidity)',
                r'expoclass = XC4 (Cyclic wet and dry)',
                r'expoclass = XD1 (Moderate humidity, exposure to airborne chlorides)',
                r'expoclass = XD2 (Wet, rarely dry, exposure to chlorides)',
                r'expoclass = XD3 (Cyclic wet and dry, exposure to chlorides)',
                r'expoclass = XS1 (Exposed to airborne salt but not in direct contact with sea water)',
                r'expoclass = XS2 (Permanently submerged)',
                r'expoclass = XS3 (Tidal, splash, and spray zones)',
            ],
            [
                r'S = 1',
                r'S = 2',
                r'S = 3',
                r'S = 4',
                r'S = 5',
                r'S = 6',
            ],
        ],
        'data': [
            [
                r'c_{min,dur} = 10', r'c_{min,dur} = 10', r'c_{min,dur} = 10', r'c_{min,dur} = 10', r'c_{min,dur} = 15', r'c_{min,dur} = 20'
            ],
            [
                r'c_{min,dur} = 10', r'c_{min,dur} = 10', r'c_{min,dur} = 10', r'c_{min,dur} = 15', r'c_{min,dur} = 20', r'c_{min,dur} = 25'
            ],
            [
                r'c_{min,dur} = 10', r'c_{min,dur} = 15', r'c_{min,dur} = 20', r'c_{min,dur} = 25', r'c_{min,dur} = 30', r'c_{min,dur} = 35'
            ],
            [
                r'c_{min,dur} = 10', r'c_{min,dur} = 15', r'c_{min,dur} = 20', r'c_{min,dur} = 25', r'c_{min,dur} = 30', r'c_{min,dur} = 35'
            ],
            [
                r'c_{min,dur} = 15', r'c_{min,dur} = 20', r'c_{min,dur} = 25', r'c_{min,dur} = 30', r'c_{min,dur} = 35', r'c_{min,dur} = 40'
            ],
            [
                r'c_{min,dur} = 20', r'c_{min,dur} = 25', r'c_{min,dur} = 30', r'c_{min,dur} = 35', r'c_{min,dur} = 40', r'c_{min,dur} = 45'
            ],
            [
                r'c_{min,dur} = 25', r'c_{min,dur} = 30', r'c_{min,dur} = 35', r'c_{min,dur} = 40', r'c_{min,dur} = 45', r'c_{min,dur} = 50'
            ],
            [
                r'c_{min,dur} = 30', r'c_{min,dur} = 35', r'c_{min,dur} = 40', r'c_{min,dur} = 45', r'c_{min,dur} = 50', r'c_{min,dur} = 55'
            ],
            [
                r'c_{min,dur} = 20', r'c_{min,dur} = 25', r'c_{min,dur} = 30', r'c_{min,dur} = 35', r'c_{min,dur} = 40', r'c_{min,dur} = 45'
            ],
            [
                r'c_{min,dur} = 25', r'c_{min,dur} = 30', r'c_{min,dur} = 35', r'c_{min,dur} = 40', r'c_{min,dur} = 45', r'c_{min,dur} = 50'
            ],
            [
                r'c_{min,dur} = 30', r'c_{min,dur} = 35', r'c_{min,dur} = 40', r'c_{min,dur} = 45', r'c_{min,dur} = 50', r'c_{min,dur} = 55'
            ],
        ],
    },
]

content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/89786720/EN1992-1-1+Reinforced+Concrete+Cover
        'id': '19',
        'standard_type': 'EUROCODE',
        'standard': 'EN1992-1-1',
        'standard_name': 'Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings',
        'title': 'Reinforced Concrete Cover Calculation According to Eurocode',
        'description': "[EN1992-1-1] This calculation guide provides a step-by-step process for selecting appropriate exposure classes and determining the minimum concrete cover to ensure the durability of reinforced concrete structures. It is based on the Eurocode standards for durability and cover to reinforcement. The guide includes considerations for environmental conditions, exposure to aggressive elements, and other factors that could affect the long-term performance of the concrete and reinforcement.",
        'edition': '2004',
        'target_components': ['G19_COMP_3', 'G19_COMP_7'],
        'test_input': [
            {'component': 'G14_COMP_4', 'value': 'C12/15'}, # C = C12/15
            {'component': 'G19_COMP_1', 'value': 'X0 (No risk of corrosion or attack)'}, # expoclass = X0 (No risk of corrosion or attack)
            # {'component': 'G19_COMP_1', 'value': 'XC1 (Dry or permanently wet)'}, # expoclass = XC1 (Dry or permanently wet)
            {'component': 'G19_COMP_2', 'value': 'General case'}, # castcond = General case
            # {'component': 'G19_COMP_2', 'value': 'Prepared ground'}, # castcond = Prepared ground
            # {'component': 'G19_COMP_2', 'value': 'Direct soil'}, # castcond = Direct soil
            {'component': 'G19_COMP_8', 'value': 'Exposed Aggregate'}, # unsurtype = Exposed Aggregate
            # {'component': 'G19_COMP_8', 'value': 'None'}, # unsurtype = None
            {'component': 'G19_COMP_10', 'value': 'None'}, # abraclass = None
            # {'component': 'G19_COMP_10', 'value': 'XM1 (Moderate abrasion: vehicles with air tires)'}, # abraclass = XM1 (Moderate abrasion: vehicles with air tires)
            # {'component': 'G19_COMP_10', 'value': 'XM2 (Heavy abrasion: forklifts with air or rubber tires)'}, # abraclass = XM2 (Heavy abrasion: forklifts with air or rubber tires)
            # {'component': 'G19_COMP_10', 'value': 'XM3 (Extreme abrasion: forklifts with steel tires or track vehicles)'}, # abraclass = XM3 (Extreme abrasion: forklifts with steel tires or track vehicles)
            {'component': 'G19_COMP_15', 'value': 'Separated'}, # bararrange = Separated
            # {'component': 'G19_COMP_15', 'value': 'Bundled'}, # bararrange = Bundled
            {'component': 'G19_COMP_16', 'value': '8'}, # \phi = 8
            # {'component': 'G19_COMP_16', 'value': '10'}, # \phi = 10
            {'component': 'G19_COMP_17', 'value': '2'}, # n_{b} = 2
            # {'component': 'G19_COMP_17', 'value': '3'}, # n_{b} = 3
            # {'component': 'G19_COMP_17', 'value': '4'}, # n_{b} = 4
            {'component': 'G19_COMP_19', 'value': 'exceeds 32 mm'}, # maxaggre = exceeds 32 mm
            # {'component': 'G19_COMP_19', 'value': 'does not exceed 32 mm'}, # maxaggre = does not exceed 32 mm
            {'component': 'G19_COMP_23', 'value': 'less than 100 years'}, # wolife = less than 100 years
            # {'component': 'G19_COMP_23', 'value': '100 years or more'}, # wolife = 100 years or more
            {'component': 'G19_COMP_26', 'value': 'Slab Geometry'}, # slabop = Slab Geometry
            # {'component': 'G19_COMP_26', 'value': 'Non-Slab Geometry'}, # slabop = Non-Slab Geometry
            {'component': 'G19_COMP_28', 'value': 'Special quality control ensured'}, # qualcon = Special quality control ensured
            # {'component': 'G19_COMP_28', 'value': 'Standard quality control'}, # qualcon = Standard quality control
        ],
    },
]

