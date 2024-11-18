def computed_property(*dependencies):
    """
    Decorator para criar uma propriedade computada com cache automático.

    Args:
        *dependencies: Nomes dos atributos da classe que a propriedade computada depende.
    """

    def decorator(func):
        cache_key = f"_{func.__name__}_cache"
        value_key = f"_{func.__name__}_value"


        def getter(self):
            """
            Obtém o valor da propriedade computada, recalculando-a apenas se necessário.
            """
            current_values = _get_dependency_values(self, dependencies)

            if not _is_cache_valid(self, cache_key, current_values):
                _update_cache(self, cache_key, current_values, value_key, func)

            return getattr(self, value_key)

        def setter(self, value):
            """
            Define o valor diretamente para a dependência se houver apenas uma.
            """
            if len(dependencies) == 1:
                setattr(self, dependencies[0], value)
            else:
                raise AttributeError("Cannot directly set a computed property with multiple dependencies.")

        def deleter(self):
            """
            Invalida o cache da propriedade computada.
            """
            _invalidate_cache(self, cache_key, value_key)

        return property(getter, setter, deleter, func.__doc__)

    return decorator


def _get_dependency_values(instance, dependencies):
    """
    Obtém os valores atuais das dependências da instância.

    Args:
        instance: Objeto da classe que possui a propriedade.
        dependencies: Lista de nomes das dependências.

    Returns:
        Uma tupla com os valores das dependências.
    """

    return tuple(getattr(instance, dep, None) for dep in dependencies)


def _is_cache_valid(instance, cache_key, current_values):
    """
    Verifica se o cache está válido comparando os valores atuais das dependências.

    Args:
        instance: Objeto da classe que possui a propriedade.
        cache_key: Nome do atributo que armazena o estado do cache.
        current_values: Valores atuais das dependências.

    Returns:
        True se o cache estiver válido, False caso contrário.
    """

    return getattr(instance, cache_key, None) == current_values


def _update_cache(instance, cache_key, current_values, value_key, func):
    """
    Atualiza o cache da propriedade computada com novos valores.

    Args:
        instance: Objeto da classe que possui a propriedade.
        cache_key: Nome do atributo que armazena o estado do cache.
        current_values: Valores atuais das dependências.
        value_key: Nome do atributo que armazena o valor computado.
        func: Função que computa o valor da propriedade.
    """
    setattr(instance, cache_key, current_values)
    setattr(instance, value_key, func(instance))


def _invalidate_cache(instance, cache_key, value_key):
    """
    Invalida o cache da propriedade computada.

    Args:
        instance: Objeto da classe que possui a propriedade.
        cache_key: Nome do atributo que armazena o estado do cache.
        value_key: Nome do atributo que armazena o valor computado.
    """
    setattr(instance, cache_key, None)
    setattr(instance, value_key, None)




# from math import sqrt
# class Vector:
#     def __init__(self, x, y, z, color=None):
#         self.x, self.y, self.z = x, y, z
#         self.color = color

#     @computed_property('x', 'y', 'z')
#     def magnitude(self):
#         print('computing magnitude')
#         return sqrt(self.x**2 + self.y**2 + self.z**2)
    
# v = Vector(9, 2, 6)


# class Circle:
#     def __init__(self, radius=1):
#         self.radius = radius
    
#     @computed_property('radius', 'area')
#     def diameter(self):
#         return self.radius * 2


# circle = Circle()
# print(circle.diameter)


class Circle:
    def __init__(self, radius=1):
        self.radius = radius

    @computed_property('radius')
    def diameter(self):
        return self.radius * 2
    
    @diameter.setter
    def diameter(self, diameter):
        self.radius = diameter / 2

    @diameter.deleter
    def diameter(self):
        self.radius = 0

circle = Circle()
print(circle.diameter)

circle.diameter = 3
print(circle.radius)

del circle.diameter
print(circle.radius)


# class Circle:
#     def __init__(self, radius=1):
#         self.radius = radius
#     @computed_property('radius')
#     def diameter(self):
#         """Circle diameter from radius"""
#         print('computing diameter')
#         return self.radius * 2

# help(Circle)
