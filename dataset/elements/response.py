import json

def get_element_info(data, field, value):
    for element in data["elements"]:
        if element[field] == value:
            return element
    return None

def element_search(element_name):
    element_name = element_name.lower().capitalize()

    with open("D:\Files\Python\AI\CURRENT_VER\dataset\elements\elements.json", "r") as elements_dataset:
        elements_data = json.load(elements_dataset)

    elements_info = get_element_info(elements_data, "name", element_name)

    if elements_info:
        description = elements_info["description"].capitalize()
        symbol = elements_info["symbol"]
        atomic_number = elements_info["atomic_number"]
        atomic_mass = elements_info["atomic_mass"]
        electron_configuration = elements_info["electron_configuration"]
        appearance = elements_info["appearance"]
        density = elements_info["density"]
        boiling_point = elements_info["boiling_point"]
        melting_point = elements_info["melting_point"]
        atomic_radius = elements_info["atomic_radius"]
        electronegativity = elements_info["electronegativity"]
        ionization_energy = elements_info["ionization_energy"]
        oxidation_states = elements_info["oxidation_states"]

        discovered_by = elements_info["discovered_by"]
        discovery_year = elements_info["discovery_year"]

        if discovery_year == "Ancient":
            discovery_str = f'{discovered_by}'
        else:
            discovery_str = f'{discovered_by} in {discovery_year}'

        # response = f'{description} Its chemical symbol is "{symbol}", and it has an atomic number of {atomic_number}. Discovered by {discovered_by}{discovery_str}.'
        
        description = elements_info["description"]
        response = f'''{description[:len(element_name)]} (symbol: {symbol}, atomic number: {atomic_number}) {description[len(element_name)+1:]}
Here are some essential details about hydrogen:
- Atomic Mass: {element_name} has an atomic mass of approximately {atomic_mass} atomic mass units (u).
- Electron Configuration: {electron_configuration}.
- Discovery: Hydrogen was discovered by the British scientist {discovery_str}.
- Appearance: {element_name} is commonly found as a {appearance}.
- Density: Its density is approximately {density:f} grams per cubic centimeter.
- Boiling Point: {element_name} boils at approximately {boiling_point} degrees Celsius.
- Melting Point: Its melting point is about {melting_point} degrees Celsius.
- Atomic Radius: The atomic radius of {element_name} is {atomic_radius} picometers (pm).
- Electronegativity: {element_name} has an electronegativity value of {electronegativity} on the Pauling scale.
- Ionization Energy: The ionization energy of {element_name}, the energy required to remove an electron from a hydrogen atom, is {ionization_energy} kJ/mol.
- Oxidation States: {element_name} can exist in oxidation states {oxidation_states}.'''

        # response = f'{element_name} (symbol: {symbol}, atomic number: {atomic_number}) is the lightest and most abundant element in the universe. It is a fundamental building block of matter and plays a crucial role in various natural processes and human activities. Here are some essential details about hydrogen:'


        return response
    else:
        return f"{element_name} not found in the dataset."

print(element_search("hydrogen"))