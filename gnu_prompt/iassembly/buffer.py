class Throw_Error(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __repr__(self):
        return self.message


class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.constants = set()  # Store constant variables
        self.persistent_values = {}  # Store persistent registers
        self.enclosing = enclosing

    # Define method to store a variable
    def define(self, name, value, is_constant=False):
        if is_constant:
            self.constants.add(name)
        self.values[name] = value

    # Get method to retrieve a variable's value
    def get(self, name):
        if name in self.values:
            return self.values[name]
        elif self.enclosing is not None:
            return self.enclosing.get(name)
        raise Throw_Error(f"Undefined variable '{name}'.")

    # Check if a variable is defined
    def is_defined(self, name):
        if name in self.values:
            return True
        if self.enclosing is not None:
            return self.enclosing.is_defined(name)
        return False

    # Assign method to update a variable's value
    def assign(self, name, value):
        if name in self.constants:
            raise Throw_Error(f"Cannot modify constant variable '{name}'.")
        
        if name in self.values:
            self.values[name] = value
        elif self.enclosing is not None:
            self.enclosing.assign(name, value)
        else:
            raise Throw_Error(f"Undefined variable '{name}'.")

    # Check if a variable is a constant
    def is_const(self, name):
        return name in self.constants

    # Methods for persistent values
    def store_persistent(self, name, value):
        """Store a value in the persistent storage."""
        self.persistent_values[name] = value

    def get_persistent(self, name):
        """Get a value from persistent storage."""
        if name in self.persistent_values:
            return self.persistent_values[name]
        raise Throw_Error(f"Persistent value '{name}' not found.")

    def has_persistent(self, name):
        """Check if a persistent value exists."""
        return name in self.persistent_values
