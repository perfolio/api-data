"""
Config file for Kenneth French's data library links
"""

from typing import Any, Dict, List

regions: List[Dict[str, Any]] = [
    {
        "name": "developed",
        "freq": [
            {
                "interval": "daily",
                "3factors": "Developed_3_Factors_Daily_CSV",
                "5factors": "Developed_5_Factors_Daily_CSV",
                "mom": "Developed_MOM_Factor_Daily_CSV",
            },
            {
                "interval": "monthly",
                "3factors": "Developed_3_Factors_CSV",
                "5factors": "Developed_5_Factors_CSV",
                "mom": "Developed_MOM_Factor_CSV",
            },
            {
                "interval": "annual",
                "3factors": "Developed_3_Factors_CSV",
                "5factors": "Developed_5_Factors_CSV",
                "mom": "Developed_MOM_Factor_CSV",
            },
        ],
    },
    {
        "name": "developed_ex_us",
        "freq": [
            {
                "interval": "daily",
                "3factors": "Developed_ex_US_3_Factors_Daily_CSV",
                "5factors": "Developed_ex_US_5_Factors_Daily_CSV",
                "mom": "Developed_ex_US_MOM_Factor_Daily_CSV",
            },
            {
                "interval": "monthly",
                "3factors": "Developed_ex_US_3_Factors_CSV",
                "5factors": "Developed_ex_US_5_Factors_CSV",
                "mom": "Developed_ex_US_MOM_Factor_CSV",
            },
            {
                "interval": "annual",
                "3factors": "Developed_ex_US_3_Factors_CSV",
                "5factors": "Developed_ex_US_5_Factors_CSV",
                "mom": "Developed_ex_US_MOM_Factor_CSV",
            },
        ],
    },
    {
        "name": "europe",
        "freq": [
            {
                "interval": "daily",
                "3factors": "Europe_3_Factors_Daily_CSV",
                "5factors": "Europe_5_Factors_Daily_CSV",
                "mom": "Europe_MOM_Factor_Daily_CSV",
            },
            {
                "interval": "monthly",
                "3factors": "Europe_3_Factors_CSV",
                "5factors": "Europe_5_Factors_CSV",
                "mom": "Europe_MOM_Factor_CSV",
            },
            {
                "interval": "annual",
                "3factors": "Europe_3_Factors_CSV",
                "5factors": "Europe_5_Factors_CSV",
                "mom": "Europe_MOM_Factor_CSV",
            },
        ],
    },
    {
        "name": "japan",
        "freq": [
            {
                "interval": "daily",
                "3factors": "Japan_3_Factors_Daily_CSV",
                "5factors": "Japan_5_Factors_Daily_CSV",
                "mom": "Japan_MOM_Factor_Daily_CSV",
            },
            {
                "interval": "monthly",
                "3factors": "Japan_3_Factors_CSV",
                "5factors": "Japan_5_Factors_CSV",
                "mom": "Japan_MOM_Factor_CSV",
            },
            {
                "interval": "annual",
                "3factors": "Japan_3_Factors_CSV",
                "5factors": "Japan_5_Factors_CSV",
                "mom": "Japan_MOM_Factor_CSV",
            },
        ],
    },
    {
        "name": "asia_pacific_ex_japan",
        "freq": [
            {
                "interval": "daily",
                "3factors": "Asia_Pacific_ex_Japan_3_Factors_Daily_CSV",
                "5factors": "Asia_Pacific_ex_Japan_5_Factors_Daily_CSV",
                "mom": "Asia_Pacific_ex_Japan_MOM_Factor_Daily_CSV",
            },
            {
                "interval": "monthly",
                "3factors": "Asia_Pacific_ex_Japan_3_Factors_CSV",
                "5factors": "Asia_Pacific_ex_Japan_5_Factors_CSV",
                "mom": "Asia_Pacific_ex_Japan_MOM_Factor_CSV",
            },
            {
                "interval": "annual",
                "3factors": "Asia_Pacific_ex_Japan_3_Factors_CSV",
                "5factors": "Asia_Pacific_ex_Japan_5_Factors_CSV",
                "mom": "Asia_Pacific_ex_Japan_MOM_Factor_CSV",
            },
        ],
    },
    {
        "name": "north_america",
        "freq": [
            {
                "interval": "daily",
                "3factors": "North_America_3_Factors_Daily_CSV",
                "5factors": "North_America_5_Factors_Daily_CSV",
                "mom": "North_America_MOM_Factor_Daily_CSV",
            },
            {
                "interval": "monthly",
                "3factors": "North_America_3_Factors_CSV",
                "5factors": "North_America_5_Factors_CSV",
                "mom": "North_America_MOM_Factor_CSV",
            },
            {
                "interval": "annual",
                "3factors": "North_America_3_Factors_CSV",
                "5factors": "North_America_5_Factors_CSV",
                "mom": "North_America_MOM_Factor_CSV",
            },
        ],
    },
    {
        "name": "emerging",
        "freq": [
            {
                "interval": "monthly",
                "5factors": "Emerging_5_Factors_CSV",
                "mom": "Emerging_MOM_Factor_CSV",
            },
            {
                "interval": "annual",
                "5factors": "Emerging_5_Factors_CSV",
                "mom": "Emerging_MOM_Factor_CSV",
            },
        ],
    },
]
