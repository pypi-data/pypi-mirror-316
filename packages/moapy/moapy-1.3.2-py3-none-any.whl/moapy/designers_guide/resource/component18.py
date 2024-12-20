component_list = [
    {
        'id': 'G18_COMP_1',
        'standard': 'EN1992-1-1',
        'reference': ['AnnexC(Table C.1)'],
        'title': 'Characteristic yield strength of reinforcement',
        'description': r"Characteristic Yield Strength is the stress level at which a material has a specified probability of yielding, typically 95%. It represents the strength below which not more than 5% of the material's test results are expected to fall, ensuring a high level of reliability in structural design.",
        'latex_symbol': r'f_{yk}',
        'type': 'number',
        'unit': 'MPa',
        'notation': 'standard',
        'decimal': 0,
        'default': 500.0,
        'limits': {'in_min': 400, 'in_max': 600},
        'use_std': False,
    },
    {
        'id': 'G18_COMP_2',
        'standard': 'EN1992-1-1',
        'reference': ['2.4.2.4(Table2.1N)'],
        'title': 'Partial factor for reinforcing or prestressing steel',
        'description': r"This factor is used in structural design to account for uncertainties in material properties, workmanship, and loading conditions. It ensures that the design remains safe even under unfavorable conditions by reducing the allowable stress or strength values of steel in calculations.",
        'latex_symbol': r'\gamma_{s}',
        'latex_equation': r'\gamma_{s} = 1.15',
        'type': 'number',
        'unit': '',
        'notation': 'standard',
        'decimal': 2,
        'required': ['G14_COMP_3'],
        'table': 'formula',
    },
    {
        'id': 'G18_COMP_3',
        'standard': 'EN1992-1-1',
        'reference': ['3.2.7(Figure 3.8)'],
        'title': 'Design yield strength of reinforcement',
        'description': r"Design Yield Strength is the reduced yield strength of a material used in structural design calculations. It is obtained by dividing the characteristic yield strength by a partial safety factor, which accounts for uncertainties in material properties and ensures the safety of the structure.",
        'latex_symbol': r'f_{yd}',
        'latex_equation': r'f_{yd} = \frac{f_{yk}}{\gamma_{s}}',
        'type': 'number',
        'unit': 'MPa',
        'notation': 'standard',
        'decimal': 3,
        'required': ['G18_COMP_1', 'G18_COMP_2'],
    },
    {
        'id': 'G18_COMP_4',
        'standard': 'EN1992-1-1',
        'reference': ['3.2.7(3)'],
        'title': 'Mean density of reinforcing steel',
        'description': r"The mean density of reinforcing steel represents the average mass per unit volume of the steel used in reinforced concrete structures. It is a critical parameter in structural design and is used to calculate the weight of the steel reinforcement in a structure.",
        'latex_symbol': r'\rho_{s}',
        'type': 'number',
        'unit': 'kg/m^3',
        'notation': 'standard',
        'decimal': 0,
        'default': 7850.0,
        'const': True,
    },
    {
        'id': 'G18_COMP_5',
        'standard': 'EN1992-1-1',
        'reference': ['3.2.7(4)'],
        'title': 'Modulus of elasticity for reinforcing steel',
        'description': r"The modulus of elasticity for reinforcing steel represents the stiffness of the steel used in structural calculations. It measures the steel's ability to deform elastically (i.e., return to its original shape) under load and is used to calculate deflections, stresses, and other important factors in structural design.",
        'latex_symbol': r'E_{s}',
        'type': 'number',
        'unit': 'MPa',
        'notation': 'standard',
        'decimal': 0,
        'default': 200000.0,
        'const': True,
    },
    {
        'id': 'G18_COMP_6',
        'standard': 'EN1992-1-1',
        'reference': ['3.2.7(Figure 3.8)'],
        'title': 'Design yield strain of reinforcing steel',
        'description': r"Design Yield Strain of reinforcing steel is the strain corresponding to the design yield strength in structural calculations. It represents the level of strain at which the steel begins to yield under the applied load, and is a critical parameter in determining the deformation behavior of the structure.",
        'latex_symbol': r'\epsilon_{yd}',
        'latex_equation': r'\epsilon_{yd} = (\frac{f_{yd}}{E_{s}}) \times 100',
        'type': 'number',
        'unit': '%',
        'notation': 'standard',
        'decimal': 3,
        'required': ['G18_COMP_3', 'G18_COMP_5'],
    },
    {
        'id': 'G18_COMP_7',
        'standard': 'EN1992-1-1',
        'reference': ['3.2.4(2)'],
        'title': 'Normal design stress-strain model selection',
        'description': r"This menu allows users to select the appropriate stress-strain model for normal design conditions of reinforcing steel according to Eurocode guidelines. It offers options for both inclined and horizontal top branch models, ensuring that the chosen model aligns with the specific reinforcing steel class and design requirements.",
        'latex_symbol': r'rebarss',
        'type': 'string',
        'unit': '',
        'notation': 'text',
        'default': 'Elastic-Perfectly Plastic (horizontal top branch)',
        'table': 'dropdown',
    },
    {
        'id': 'G18_COMP_8',
        'standard': 'EN1992-1-1',
        'reference': ['AnnexC(Table C.1)'],
        'title': 'Minimum value of the tensile to yield strength ratio',
        'description': r"The minimum k value represents the ratio of tensile strength to yield strength in reinforcing steel. It indicates the level of strain hardening the steel undergoes after yielding, with higher values of k reflecting greater ductility and capacity for additional load-bearing.",
        'latex_symbol': r'k',
        'latex_equation': r'k = 1.00',
        'type': 'number',
        'unit': '',
        'notation': 'standard',
        'decimal': 2,
        'required': ['G18_COMP_7'],
        'table': 'formula',
    },
    {
        'id': 'G18_COMP_9',
        'standard': 'EN1992-1-1',
        'reference': ['AnnexC(Table C.1)'],
        'title': 'Characteristic strain of reinforcement steel at maximum load',
        'description': r"Ultimate Strain at Maximum Stress refers to the strain experienced by reinforcing steel at the point of maximum stress before failure. It is a key indicator of the material's ductility, showing how much deformation the steel can undergo before reaching its ultimate strength.",
        'latex_symbol': r'\epsilon_{uk}',
        'latex_equation': r'\epsilon_{uk} = 0',
        'type': 'number',
        'unit': '%',
        'notation': 'standard',
        'decimal': 3,
        'required': ['G18_COMP_7'],
        'table': 'formula',
    },
    {
        'id': 'G18_COMP_10',
        'standard': 'EN1992-1-1',
        'reference': ['3.2.7 (2)'],
        'title': 'Design limit strain of reinforcing stee',
        'description': r"Design Limit Strain of reinforcing steel is the maximum strain that the steel is expected to endure in structural design without failure. It represents the strain limit considered in design calculations to ensure that the structure remains safe under extreme loading conditions.",
        'latex_symbol': r'\epsilon_{ud}',
        'latex_equation': r'\epsilon_{uk} = 0',
        'type': 'number',
        'unit': '%',
        'notation': 'standard',
        'decimal': 3,
        'required': ['G18_COMP_9'],
        'table': 'formula',
    },
]
data_table = [
    {
        'id': 'G18_COMP_2',
        'criteria': [
            [
                r'designsitu = Persistent',
                r'designsitu = Transient',
                r'designsitu = Accidental',
            ]
        ],
        'data': [
            r'\gamma_{s} = 1.15',
            r'\gamma_{s} = 1.15',
            r'\gamma_{s} = 1.00'
        ],
    },
    {
        'id': 'G18_COMP_7',
        'enum': [
            {'label': 'Elastic-Perfectly Plastic (horizontal top branch)'},
            {'label': '(Class A) Elastic-Plastic with Hardening'},
            {'label': '(Class B) Elastic-Plastic with Hardening'},
            {'label': '(Class C) Elastic-Plastic with Hardening'},
        ],
    },
    {
        'id': 'G18_COMP_8',
        'criteria': [
            [
                r'rebarss = Elastic-Perfectly Plastic (horizontal top branch)',
                r'rebarss = (Class A) Elastic-Plastic with Hardening',
                r'rebarss = (Class B) Elastic-Plastic with Hardening',
                r'rebarss = (Class C) Elastic-Plastic with Hardening',
            ]
        ],
        'data': [
            r'k = 1.00',
            r'k = 1.05',
            r'k = 1.08',
            r'k = 1.15',
        ],
    },
    {
        'id': 'G18_COMP_9',
        'criteria': [
            [
                r'rebarss = Elastic-Perfectly Plastic (horizontal top branch)',
                r'rebarss = (Class A) Elastic-Plastic with Hardening',
                r'rebarss = (Class B) Elastic-Plastic with Hardening',
                r'rebarss = (Class C) Elastic-Plastic with Hardening',
            ]
        ],
        'data': [
            r'\epsilon_{uk} = 0', # TODO : no need 나타낼 수 있도록 변경
            r'\epsilon_{uk} = 2.5',
            r'\epsilon_{uk} = 5.0',
            r'\epsilon_{uk} = 7.5',
        ],
    },
    {
        'id': 'G18_COMP_10',
        'criteria': [
            [
                r'rebarss = Elastic-Perfectly Plastic (horizontal top branch)',
                r'rebarss = (Class A) Elastic-Plastic with Hardening',
                r'rebarss = (Class B) Elastic-Plastic with Hardening',
                r'rebarss = (Class C) Elastic-Plastic with Hardening',
            ]
        ],
        'data': [
            r'\epsilon_{ud} = 0', # TODO : no need 나타낼 수 있도록 변경
            r'\epsilon_{ud} = 0.9 \times \epsilon_{uk}',
            r'\epsilon_{ud} = 0.9 \times \epsilon_{uk}',
            r'\epsilon_{ud} = 0.9 \times \epsilon_{uk}',
        ],
    },
]


content = [
    {
        # link : https://midastech.atlassian.net/wiki/spaces/RPMinovation/pages/88180711/EN1992-1-1+Reinforcing+Steel+Design+Parameters
        'id': '18',
        'standard_type': 'EUROCODE',
        'standard': 'EN1992-1-1',
        'standard_name': 'Eurocode 2: Design of concrete structures — Part 1-1: General rules and rules for buildings',
        'title': 'Reinforcing Steel Design Parameters',
        'description': "[EN1992-1-1] This guide outlines the process for calculating the necessary reinforcing steel parameters based on Eurocode standards. It details the steps to determine design yield strength, ultimate design strain, and characteristic strain limits for reinforcing steel, ensuring compliance with structural safety and performance requirements.",
        'edition': '2004',
        'target_components': ['G18_COMP_3', 'G18_COMP_6', 'G18_COMP_10'],
        'test_input': [
            {'component': 'G14_COMP_3', 'value': 'Persistent'}, # designsitu = Persistent
            # {'component': "G14_COMP_3", 'value': 'Transient'}, # designsitu = Transient
            # {'component': "G14_COMP_3", 'value': 'Accidental'}, # designsitu = Accidental
            {'component': 'G18_COMP_1', 'value': 500},
            {'component': 'G18_COMP_7', 'value': 'Elastic-Perfectly Plastic (horizontal top branch)'}, # rebarss = Elastic-Perfectly Plastic (horizontal top branch)
            # {'component': 'G18_COMP_7', 'value': '(Class A) Elastic-Plastic with Hardening'}, # rebarss = (Class A) Elastic-Plastic with Hardening
            # {'component': 'G18_COMP_7', 'value': '(Class B) Elastic-Plastic with Hardening'}, # rebarss = (Class B) Elastic-Plastic with Hardening
            # {'component': 'G18_COMP_7', 'value': '(Class C) Elastic-Plastic with Hardening'}, # rebarss = (Class C) Elastic-Plastic with Hardening
        ],
    },
]
