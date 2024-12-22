import pytest
from at_common_workflow.types.meta import (
    AllowedTypes, ValidatedDict, Schema, Mappings, Arguments
)

class TestAllowedTypes:
    def test_get_types(self):
        types = AllowedTypes.get_types()
        assert isinstance(types, tuple)
        assert str in types
        assert int in types
        assert float in types
        assert bool in types
        assert dict in types
        assert list in types

    def test_get_type_map(self):
        type_map = AllowedTypes.get_type_map()
        assert isinstance(type_map, dict)
        assert type_map['str'] == str
        assert type_map['int'] == int
        assert type_map['float'] == float
        assert type_map['bool'] == bool
        assert type_map['dict'] == dict
        assert type_map['list'] == list

class TestSchema:
    def test_schema_serialization(self):
        schema = Schema({'key': str})
        serialized = schema.to_dict()
        assert serialized == {'key': 'str'}
        
        deserialized = Schema.from_dict(serialized)
        assert isinstance(deserialized, Schema)
        assert dict(deserialized) == {'key': str}

    def test_invalid_type_name(self):
        with pytest.raises(KeyError):
            Schema.from_dict({'key': 'invalid_type'})

class TestMappings:
    def test_schema_validation(self):
        source_schema = Schema({'input': str})
        target_schema = Schema({'output': str})
        
        # Valid mapping
        valid_mapping = Mappings(
            {'input': 'output'}, 
            source_schema=source_schema,
            target_schema=target_schema
        )
        assert dict(valid_mapping) == {'input': 'output'}
        
        # Invalid source key
        with pytest.raises(KeyError, match="Mapping source 'invalid' not found in schema"):
            Mappings(
                {'invalid': 'output'},
                source_schema=source_schema,
                target_schema=target_schema
            )
        
        # Invalid target key
        with pytest.raises(KeyError, match="Mapping target 'invalid' not found in schema"):
            Mappings(
                {'input': 'invalid'},
                source_schema=source_schema,
                target_schema=target_schema
            )

    def test_mappings_serialization(self):
        mappings = Mappings({'source': 'target'})
        serialized = mappings.to_dict()
        assert serialized == {'source': 'target'}
        
        deserialized = Mappings.from_dict(serialized)
        assert isinstance(deserialized, Mappings)
        assert dict(deserialized) == {'source': 'target'}

class TestArguments:
    def test_none_value_validation(self):
        with pytest.raises(ValueError, match="Argument 'key' cannot be None"):
            Arguments({'key': None})

    def test_type_validation_with_allowed_types(self):
        # Test all allowed types
        valid_args = {
            'str_val': 'string',
            'int_val': 42,
            'float_val': 3.14,
            'bool_val': True,
            'dict_val': {'nested': 'value'},
            'list_val': [1, 2, 3]
        }
        args = Arguments(valid_args)
        assert dict(args) == valid_args

        # Test invalid type
        class CustomType:
            pass

        with pytest.raises(TypeError, match="Invalid type for argument 'invalid'"):
            Arguments({'invalid': CustomType()})

class TestValidatedDict:
    def test_abstract_class(self):
        with pytest.raises(TypeError):
            ValidatedDict({})  # Cannot instantiate abstract class

    def test_to_dict_conversion(self):
        class ConcreteDict(ValidatedDict[str]):
            def _validate(self, data):
                pass

        data = {'key': 'value'}
        validated = ConcreteDict(data)
        assert validated.to_dict() == data 