import allure
import pytest
from utils.schema_validator import validate_response

PROJECT_ID = 12115
PRODUCTS_PATH = "/collections/products/records"


@allure.feature("Products")
class TestGetProducts:

    @allure.title("GET /collections/products/records returns 200")
    @pytest.mark.smoke
    def test_returns_200(self, reqres_api):
        response = reqres_api.get(PRODUCTS_PATH, params={"project_id": PROJECT_ID})
        assert response.status_code == 200

    @allure.title("Response body matches JSON schema")
    @pytest.mark.smoke
    def test_response_matches_schema(self, reqres_api):
        response = reqres_api.get(PRODUCTS_PATH, params={"project_id": PROJECT_ID})
        assert response.status_code == 200
        validate_response(response.json(), "products")

    @allure.title("Response contains data list and meta object")
    @pytest.mark.regression
    def test_response_top_level_keys(self, reqres_api):
        response = reqres_api.get(PRODUCTS_PATH, params={"project_id": PROJECT_ID})
        body = response.json()
        assert "data" in body, "Missing 'data' key"
        assert "meta" in body, "Missing 'meta' key"
        assert isinstance(body["data"], list)
        assert isinstance(body["meta"], dict)

    @allure.title("Meta object contains correct pagination fields")
    @pytest.mark.regression
    def test_meta_pagination_fields(self, reqres_api):
        response = reqres_api.get(PRODUCTS_PATH, params={"project_id": PROJECT_ID})
        meta = response.json()["meta"]
        assert meta["page"] == 1
        assert meta["limit"] > 0
        assert meta["total"] >= 0
        assert meta["pages"] >= 1

    @allure.title("Meta total matches actual number of items in data")
    @pytest.mark.regression
    def test_meta_total_matches_data_length(self, reqres_api):
        response = reqres_api.get(PRODUCTS_PATH, params={"project_id": PROJECT_ID})
        body = response.json()
        assert body["meta"]["total"] == len(body["data"])

    @allure.title("Each product record has required fields with correct types")
    @pytest.mark.regression
    def test_product_record_structure(self, reqres_api):
        response = reqres_api.get(PRODUCTS_PATH, params={"project_id": PROJECT_ID})
        records = response.json()["data"]
        assert len(records) > 0, "Expected at least one product record"
        for record in records:
            assert isinstance(record["id"], str)
            assert isinstance(record["collection_id"], str)
            assert record["project_id"] == PROJECT_ID
            assert isinstance(record["created_at"], str)
            assert isinstance(record["updated_at"], str)

    @allure.title("Each product data object has correct field types")
    @pytest.mark.regression
    def test_product_data_field_types(self, reqres_api):
        response = reqres_api.get(PRODUCTS_PATH, params={"project_id": PROJECT_ID})
        records = response.json()["data"]
        for record in records:
            product = record["data"]
            assert isinstance(product["name"], str), f"name must be a string, got {type(product['name'])}"
            assert isinstance(product["price"], (int, float)), f"price must be a number, got {type(product['price'])}"
            assert product["price"] > 0, f"price must be positive, got {product['price']}"
            assert isinstance(product["category"], str), f"category must be a string, got {type(product['category'])}"
            assert isinstance(product["in_stock"], bool), f"in_stock must be a bool, got {type(product['in_stock'])}"

    @allure.title("Response time is under 3 seconds")
    @pytest.mark.smoke
    def test_response_time(self, reqres_api):
        response = reqres_api.get(PRODUCTS_PATH, params={"project_id": PROJECT_ID})
        elapsed = response.elapsed.total_seconds()
        assert elapsed < 3, f"Response took {elapsed:.2f}s, expected < 3s"

    @allure.title("Response Content-Type is application/json")
    @pytest.mark.regression
    def test_content_type_is_json(self, reqres_api):
        response = reqres_api.get(PRODUCTS_PATH, params={"project_id": PROJECT_ID})
        assert "application/json" in response.headers.get("Content-Type", "")

    @allure.title("All records belong to the requested project_id")
    @pytest.mark.regression
    def test_all_records_belong_to_project(self, reqres_api):
        response = reqres_api.get(PRODUCTS_PATH, params={"project_id": PROJECT_ID})
        for record in response.json()["data"]:
            assert record["project_id"] == PROJECT_ID

    @allure.title("Request without project_id still returns 200 with records")
    @pytest.mark.regression
    def test_missing_project_id(self, reqres_api):
        response = reqres_api.get(PRODUCTS_PATH)
        assert response.status_code == 200
        body = response.json()
        assert "data" in body
        assert "meta" in body

    @allure.title("Products list with known categories")
    @pytest.mark.regression
    @pytest.mark.parametrize("category", ["Electronics", "Stationery", "Food & Drink"])
    def test_known_categories_present(self, reqres_api, category):
        response = reqres_api.get(PRODUCTS_PATH, params={"project_id": PROJECT_ID})
        categories = [r["data"]["category"] for r in response.json()["data"]]
        assert category in categories, f"Expected category '{category}' not found in {categories}"
