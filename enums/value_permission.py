from enum import Enum

class ValuePermission(Enum):
    EDIT_RIDDLES = 1
    DELETE_RIDDLES = 2
    ADD_RIDDLES = 3
    
    def get_all_permissions():
        return [p.value for p in ValuePermission] #TRAE LOS VALORES DE LOS PERMISSIONS, NO LOS NOMBRES, PORQUE EN LA DB SE GUARDAN LOS VALORES