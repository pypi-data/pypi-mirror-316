import pytest
from pathlib import Path
from sqldeps import SQLDependencyExtractor

# Basic query tests
def test_simple_select():
    extractor = SQLDependencyExtractor()
    sql = "SELECT id, name FROM users"
    
    result = extractor.extract_from_query(sql)
    
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
    
    result = extractor.extract_from_query(sql)
    
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
    
    result = extractor.extract_from_query(sql)
    
    assert result.tables == {'users', 'orders'}
    assert 'user_orders' not in result.tables  # CTE should not be in tables

# File-based tests
@pytest.fixture
def sql_files(tmp_path):
    # Create a temporary directory for test files
    test_dir = tmp_path / "test_sql"
    test_dir.mkdir()
    
    # Simple query file
    simple_file = test_dir / "simple.sql"
    simple_file.write_text("""
    SELECT id, name 
    FROM users;
    """)
    
    # Multiple statements file
    multi_file = test_dir / "multi.sql"
    multi_file.write_text("""
    CREATE TEMPORARY TABLE temp_orders AS
    SELECT customer_id, COUNT(*) as order_count
    FROM orders
    GROUP BY customer_id;

    SELECT u.name, t.order_count
    FROM users u
    JOIN temp_orders t ON u.id = t.customer_id
    WHERE t.order_count > 5;
    """)
    
    # Function definition file
    function_file = test_dir / "function.sql"
    function_file.write_text("""
    CREATE OR REPLACE FUNCTION get_active_users()
    RETURNS TABLE (
        user_id INTEGER,
        user_name TEXT,
        order_count BIGINT
    ) AS $function$
    BEGIN
        RETURN QUERY
        SELECT u.id, u.name, COUNT(o.id)
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE u.active = true
        GROUP BY u.id, u.name;
    END;
    $function$;
    """)
    
    return test_dir

def test_extract_from_simple_file(sql_files):
    extractor = SQLDependencyExtractor()
    result = extractor.extract_from_file(sql_files / "simple.sql")
    
    assert result.tables == {'users'}
    assert result.columns == {'users': {'id', 'name'}}
    assert "SELECT id, name" in result.query

def test_extract_from_multi_statement_file(sql_files):
    extractor = SQLDependencyExtractor()
    result = extractor.extract_from_file(sql_files / "multi.sql")
    
    # Check tables (both orders and users should be included)
    assert result.tables == {'orders', 'users'}
    assert 'temp_orders' not in result.tables  # Temporary table should not be included

def test_extract_from_function_file(sql_files):
    extractor = SQLDependencyExtractor()
    result = extractor.extract_from_file(sql_files / "function.sql")
    
    assert result.tables == {'users', 'orders'}
    assert result.columns == {
        'users': {'id', 'name', 'active'},
        'orders': {'id', 'user_id'}
    }

def test_file_not_found():
    extractor = SQLDependencyExtractor()
    with pytest.raises(FileNotFoundError):
        extractor.extract_from_file("nonexistent.sql")

def test_empty_script():
    extractor = SQLDependencyExtractor()
    result = extractor.extract_from_script("")
    assert result.tables == set()
    assert result.columns == {}

def test_script_with_comments():
    extractor = SQLDependencyExtractor()
    sql = """
    -- This is a comment
    /* This is a 
       multiline comment */
    SELECT id, name FROM users;
    """
    result = extractor.extract_from_script(sql)
    
    assert result.tables == {'users'}
    assert result.columns == {'users': {'id', 'name'}}

def test_script_with_schema_qualified_tables():
    extractor = SQLDependencyExtractor()
    sql = """
    SELECT u.id, u.name, o.order_date
    FROM public.users u
    JOIN sales.orders o ON u.id = o.user_id;
    """
    result = extractor.extract_from_script(sql)
    
    assert result.tables == {'public.users', 'sales.orders'}
    assert result.columns == {
        'public.users': {'id', 'name'},
        'sales.orders': {'order_date', 'user_id'}
    }

def test_multiple_queries_with_function_and_cte():
    extractor = SQLDependencyExtractor()
    sql = """
    CREATE OR REPLACE FUNCTION make_pgi_shape_geom_clusters()
      RETURNS VOID
      LANGUAGE plpgsql
    AS $function$
    BEGIN
        -- Build table with cluster + geom data
        DROP TABLE IF EXISTS pgi_shape_geom_clusters CASCADE;
        CREATE TABLE pgi_shape_geom_clusters AS
            SELECT
                pgic."PropertyGroupId",
                pgic."ShapeGroupId",
                sh.geom,
                pgic."ShapeCluster" 
            FROM
                pgi_shape_clusters pgic
            LEFT JOIN
                spatial."Shape" sh
            ON
                pgic."PropertyGroupId" = sh."ShapeId";

        -- Integrity check: A Property observation should have at most one row
        ALTER TABLE pgi_shape_geom_clusters ADD PRIMARY KEY ("PropertyGroupId","ShapeGroupId");
        ANALYZE VERBOSE pgi_shape_geom_clusters;
    END
    $function$;

    WITH user_orders AS (
        SELECT user_id, COUNT(*) as order_count
        FROM orders
        GROUP BY user_id
    )
    SELECT u.name, uo.order_count
    FROM users u
    JOIN user_orders uo ON u.id = uo.user_id;
    """
    
    result = extractor.extract_from_query(sql)
    
    # Check that we capture dependencies from both the function and the CTE query
    expected_tables = {
        'pgi_shape_clusters', 
        'spatial.Shape', 
        'pgi_shape_geom_clusters',
        'orders',
        'users'
    }
    
    expected_columns = {
        'pgi_shape_clusters': {'ShapeGroupId', 'PropertyGroupId', 'ShapeCluster'},
        'spatial.Shape': {'ShapeId', 'geom'},
        'users': {'id', 'name'}
    }
    
    assert result.tables == expected_tables
    assert result.columns == expected_columns
