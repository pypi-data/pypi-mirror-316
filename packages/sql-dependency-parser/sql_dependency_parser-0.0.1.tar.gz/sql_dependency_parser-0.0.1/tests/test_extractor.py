import pytest
from sqldeps import SQLDependencyExtractor

def test_simple_select():
    extractor = SQLDependencyExtractor()
    sql = "SELECT id, name FROM users"
    
    result = extractor.extract_from_query(sql)[0]
    
    assert result.tables == {'users'}
    assert result.columns == {'users': {'id', 'name'}}
    assert result.query == sql

def test_with_joins():
    extractor = SQLDependencyExtractor()
    sql = """
    SELECT u.id, u.name, o.order_id
    FROM users u
    JOIN orders o ON u.id = o.user_id
    """
    
    result = extractor.extract_from_query(sql)[0]
    
    assert result.tables == {'users', 'orders'}
    assert result.columns == {
        'users': {'id', 'name'},
        'orders': {'order_id', 'user_id'}
    }

def test_with_cte():
    extractor = SQLDependencyExtractor()
    sql = """
    WITH user_orders AS (
        SELECT user_id, COUNT(*) as order_count
        FROM orders
        GROUP BY user_id
    )
    SELECT u.name, uo.order_count
    FROM users u
    JOIN user_orders uo ON u.id = uo.user_id
    """
    
    result = extractor.extract_from_query(sql)[0]
    
    assert result.tables == {'users', 'orders'}
    assert 'user_orders' not in result.tables  # CTE should not be in tables
