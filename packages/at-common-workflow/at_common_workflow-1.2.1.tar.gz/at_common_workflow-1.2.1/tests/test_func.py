import pytest
from at_common_workflow.core.func import Func
from at_common_workflow.types.meta import MetaFunc
import asyncio
from unittest.mock import Mock, patch

# Test fixtures and helper functions
def sync_func_dict(*args, **kwargs):
    return {"result": "sync"}

def sync_func_none(*args, **kwargs):
    return None

def sync_func_invalid(*args, **kwargs):
    return "invalid"

async def async_func_dict(*args, **kwargs):
    return {"result": "async"}

async def async_func_none(*args, **kwargs):
    return None

async def async_func_invalid(*args, **kwargs):
    return "invalid"

class TestClass:
    def method_dict(self):
        return {"result": "method"}

# Define ComplexClass at module level
class ComplexClass:
    def __init__(self, value):
        self.value = value
    
    def complex_method(self, multiplier):
        return {"result": self.value * multiplier}

# Define at module level
class StaticMethodClass:
    @staticmethod
    def static_method():
        return {"result": "static"}

class TestFunc:
    
    # Test synchronous function calls
    @pytest.mark.asyncio
    async def test_sync_func_dict(self):
        func = Func(sync_func_dict)
        result = await func()
        assert result == {"result": "sync"}

    @pytest.mark.asyncio
    async def test_sync_func_none(self):
        func = Func(sync_func_none)
        result = await func()
        assert result is None

    @pytest.mark.asyncio
    async def test_sync_func_with_args(self):
        def sync_with_args(a, b, c=3):
            return {"sum": a + b + c}
        
        func = Func(sync_with_args)
        result = await func(1, 2, c=4)
        assert result == {"sum": 7}

    @pytest.mark.asyncio
    async def test_async_func_dict(self):
        func = Func(async_func_dict)
        result = await func()
        assert result == {"result": "async"}

    @pytest.mark.asyncio
    async def test_async_func_none(self):
        func = Func(async_func_none)
        result = await func()
        assert result is None

    # Test method calls
    @pytest.mark.asyncio
    async def test_method_call(self):
        test_instance = TestClass()
        func = Func(test_instance.method_dict)
        result = await func()
        assert result == {"result": "method"}

    # Test meta conversion
    def test_to_meta_function(self):
        func = Func(sync_func_dict)
        meta = func.to_meta()
        assert isinstance(meta, MetaFunc)
        assert meta.module == sync_func_dict.__module__
        assert meta.name == sync_func_dict.__name__

    def test_to_meta_method(self):
        test_instance = TestClass()
        func = Func(test_instance.method_dict)
        meta = func.to_meta()
        assert isinstance(meta, MetaFunc)
        assert meta.module == TestClass.__module__
        assert meta.name == f"{TestClass.__name__}.method_dict"

    # Test from_meta
    @pytest.mark.asyncio
    async def test_from_meta(self):
        # First convert to meta
        original_func = Func(sync_func_dict)
        meta = original_func.to_meta()
        
        # Then create new func from meta
        new_func = Func.from_meta(meta)
        
        # Test the new function
        result = await new_func()
        assert result == {"result": "sync"}

    # Test error cases
    def test_invalid_meta_module(self):
        invalid_meta = MetaFunc(module="nonexistent_module", name="some_func")
        with pytest.raises(ImportError):
            Func.from_meta(invalid_meta)

    def test_invalid_meta_name(self):
        invalid_meta = MetaFunc(module=sync_func_dict.__module__, name="nonexistent_func")
        with pytest.raises(AttributeError):
            Func.from_meta(invalid_meta)

    # Test error handling for coroutine execution
    @pytest.mark.asyncio
    async def test_sync_func_execution_error(self):
        def failing_sync_func():
            raise ValueError("Sync execution failed")
        
        func = Func(failing_sync_func)
        with pytest.raises(ValueError, match="Sync execution failed"):
            await func()

    @pytest.mark.asyncio
    async def test_async_func_execution_error(self):
        async def failing_async_func():
            raise ValueError("Async execution failed")
        
        func = Func(failing_async_func)
        with pytest.raises(ValueError, match="Async execution failed"):
            await func()

    # Test nested method calls
    @pytest.mark.asyncio
    async def test_nested_method_call(self):
        class NestedClass:
            class InnerClass:
                def inner_method(self):
                    return {"result": "nested"}
            
            def __init__(self):
                self.inner = self.InnerClass()

        nested_instance = NestedClass()
        func = Func(nested_instance.inner.inner_method)
        result = await func()
        assert result == {"result": "nested"}

    # Test lambda functions
    @pytest.mark.asyncio
    async def test_lambda_function(self):
        func = Func(lambda: {"result": "lambda"})
        result = await func()
        assert result == {"result": "lambda"}

    # Test event loop handling
    @pytest.mark.asyncio
    async def test_event_loop_usage(self):
        mock_loop = Mock()
        mock_loop.run_in_executor.return_value = asyncio.Future()
        mock_loop.run_in_executor.return_value.set_result({"result": "loop"})
        
        with patch('asyncio.get_event_loop', return_value=mock_loop):
            func = Func(sync_func_dict)
            result = await func()
            assert result == {"result": "loop"}
            mock_loop.run_in_executor.assert_called_once()

    # Test complex dictionary returns
    @pytest.mark.asyncio
    async def test_complex_dictionary_return(self):
        def complex_dict_func():
            return {
                "nested": {
                    "value": 1,
                    "list": [1, 2, 3]
                },
                "tuple": (1, 2),
                "set": {1, 2, 3}
            }
        
        func = Func(complex_dict_func)
        result = await func()
        assert isinstance(result, dict)
        assert result["nested"]["value"] == 1
        assert result["nested"]["list"] == [1, 2, 3]
        assert result["tuple"] == (1, 2)
        assert result["set"] == {1, 2, 3}

    # Test method chaining with to_meta and from_meta
    @pytest.mark.asyncio
    async def test_meta_roundtrip_with_complex_function(self):
        instance = ComplexClass(5)
        original_func = Func(instance.complex_method)
        
        # Convert to meta and back
        meta = original_func.to_meta()
        new_func = Func.from_meta(meta)
        
        # This should fail because the reconstructed method is unbound
        with pytest.raises(TypeError):
            await new_func(2)  # This will fail because it's missing 'self'

    # Test meta serialization with static methods
    @pytest.mark.asyncio
    async def test_meta_with_static_method(self):
        func = Func(StaticMethodClass.static_method)
        meta = func.to_meta()
        new_func = Func.from_meta(meta)
        result = await new_func()
        assert result == {"result": "static"}

    # Test empty dictionary return
    @pytest.mark.asyncio
    async def test_empty_dict_return(self):
        func = Func(lambda: {})
        result = await func()
        assert result == {}

    @pytest.mark.asyncio
    async def test_long_running_task_cancellation(self):
        """Test cancellation of long-running tasks"""
        async def long_running():
            await asyncio.sleep(10)
            return {"result": "done"}
        
        func = Func(long_running)
        task = asyncio.create_task(func())
        
        # Wait briefly then cancel
        await asyncio.sleep(0.1)
        task.cancel()
        
        with pytest.raises(asyncio.CancelledError):
            await task

    @pytest.mark.asyncio
    async def test_sync_func_multiple_returns(self):
        def sync_multiple_returns():
            return "result1", "result2", {"data": "value"}
        
        func = Func(sync_multiple_returns)
        result = await func()
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert result[2] == {"data": "value"}

    @pytest.mark.asyncio
    async def test_async_func_multiple_returns(self):
        async def async_multiple_returns():
            return "result1", "result2", {"data": "value"}
        
        func = Func(async_multiple_returns)
        result = await func()
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert result[2] == {"data": "value"}

    @pytest.mark.asyncio
    async def test_func_with_default_args(self):
        def func_with_defaults(a, b=2, c="default", *args, **kwargs):
            return {"a": a, "b": b, "c": c, "args": args, "kwargs": kwargs}
        
        func = Func(func_with_defaults)
        result = await func(1, c="custom", d="extra")
        assert result == {
            "a": 1,
            "b": 2,
            "c": "custom",
            "args": (),
            "kwargs": {"d": "extra"}
        }

    @pytest.mark.asyncio
    async def test_class_method(self):
        class TestClassMethod:
            @classmethod
            def class_method(cls):
                return {"result": "classmethod"}
        
        func = Func(TestClassMethod.class_method)
        result = await func()
        assert result == {"result": "classmethod"}

    @pytest.mark.asyncio
    async def test_property_method(self):
        class TestProperty:
            @property
            def prop(self):
                return {"result": "property"}
        
        instance = TestProperty()
        # Bind the property getter to the instance
        func = Func(TestProperty.prop.fget.__get__(instance, TestProperty))
        result = await func()
        assert result == {"result": "property"}

    @pytest.mark.asyncio
    async def test_concurrent_execution(self):
        async def delayed_func(delay, value):
            await asyncio.sleep(delay)
            return {"result": value}
        
        func = Func(delayed_func)
        tasks = [
            func(0.1, "first"),
            func(0.05, "second"),
            func(0.15, "third")
        ]
        
        results = await asyncio.gather(*tasks)
        assert len(results) == 3
        assert results[0] == {"result": "first"}
        assert results[1] == {"result": "second"}
        assert results[2] == {"result": "third"}

    def test_meta_with_nested_class(self):
        class Outer:
            class Inner:
                def nested_method(self):
                    return {"result": "nested"}
        
        inner = Outer.Inner()
        func = Func(inner.nested_method)
        meta = func.to_meta()
        assert meta.module == Outer.__module__
        expected_name = f"TestFunc.test_meta_with_nested_class.<locals>.{Outer.__name__}.Inner.nested_method"
        assert meta.name == expected_name

    @pytest.mark.asyncio
    async def test_generator_function(self):
        def gen_func():
            yield {"step": 1}
            yield {"step": 2}
            yield {"step": 3}
        
        with pytest.raises(TypeError, match="Generator functions are not supported"):
            Func(gen_func)  # Error should be raised here during initialization

    @pytest.mark.asyncio
    async def test_async_generator_function(self):
        async def async_gen_func():
            yield {"step": 1}
            yield {"step": 2}
            yield {"step": 3}
        
        with pytest.raises(TypeError, match="Generator functions are not supported"):
            Func(async_gen_func)  # Error should be raised here during initialization

    @pytest.mark.asyncio
    async def test_recursive_dict(self):
        def recursive_dict():
            d = {}
            d['self'] = d
            return d
        
        func = Func(recursive_dict)
        with pytest.raises(RecursionError):
            await func()