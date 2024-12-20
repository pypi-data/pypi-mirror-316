import json
import os
import unittest
from click.testing import CliRunner
from nomad_media_cli.cli import cli
from nomad_media_cli.helpers.get_content_definition_id import get_content_definition_id

class TestAssetBase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.runner = CliRunner()
#
        with open("nomad_media_cli/tests/test-config.json", "r") as file:
            test_config = json.load(file)
            cls.test_dir_id = test_config["testDirId"]
        
        #result = cls.runner.invoke(cli, [
        #    "upload-assets", 
        #    "--source", "README.md",
        #    "--id", cls.test_dir_id
        #])
        #
        #if result.exit_code != 0:
        #    raise Exception(f"Failed to upload asset: {result.output}")
        #
        #cls.asset_id = result.output.replace('"', "").strip()
        cls.asset_id = "20133c0c-19ab-4200-8609-76d9115a9304"

    @classmethod
    def setup_config(cls):
        config_path_result = cls.runner.invoke(cli, ["list-config-path"])
        if config_path_result.exit_code != 0:
            raise Exception(f"Need to run `nomad-media-cli init` before running tests")
        
        config_path = json.loads(config_path_result.output.strip())

        with open(config_path["path"], "r") as file:
            config = json.load(file)
            cls.config = config
            cls.config_path = config_path["path"]
            
    #@classmethod
    #def tearDownClass(cls):
    #    result = cls.runner.invoke(cli, [
    #        "delete-asset", 
    #        "--id", cls.asset_id
    #    ])
    #    
    #    if result.exit_code != 0:
    #        raise Exception(f"Failed to delete asset: {result.output}")
    #    
    #    print(f"Deleted asset with id: {cls.asset_id}")
        
class TestAssetUpload(TestAssetBase):
    """Tests for uploading assets"""

    #@classmethod
    #def tearDownClass(cls):
    #    result = cls.runner.invoke(cli, [
    #        "delete-asset", 
    #        "--id", cls.asset_upload_id
    #    ])
    #    
    #    if result.exit_code != 0:
    #        raise Exception(f"Failed to delete asset: {result.output}")
    #    
    #    print(f"Deleted asset with id: {cls.asset_upload_id}")
    
    def test_upload_asset(self):
        """Test asset is uploaded successfully"""
        result = self.runner.invoke(cli, [
            "upload-assets", 
            "--source", "nomad_media_cli/tests/test_files/vid.mp4",
            "--id", self.test_dir_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_id = result.output.replace('"', "").strip()
        self.assertIsNotNone(asset_id)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", asset_id
        ])
        
        self.assertEqual(asset_details_result.exit_code, 0)
        
        self.asset_upload_id = asset_id
        
    def test_upload_asset_invalid_file(self):
        """Test invalid file returns an error"""
        result = self.runner.invoke(cli, [
            "upload-assets", 
            "--source", "nomad_media_cli/tests/test_files/invalid-file",
            "--id", self.test_dir_id
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
    def test_upload_asset_empty_file(self):
        """Test empty file returns an error"""
        result = self.runner.invoke(cli, [
            "upload-assets", 
            "--source", "nomad_media_cli/tests/__init__.py",
            "--id", self.test_dir_id
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
    def test_upload_asset_invalid_id(self):
        """Test invalid ID returns an error"""
        result = self.runner.invoke(cli, [
            "upload-assets", 
            "--source", "nomad_media_cli/tests/test_files/vid.mp4",
            "--id", "invalid-id"
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
    def test_upload_asset_directory_flat(self):
        """Test uploading a directory of files with no subdirectories"""
        result = self.runner.invoke(cli, [
            "upload-assets", 
            "--source", "nomad_media_cli/tests/test_files",
            "--id", self.test_dir_id,
            "-r"
        ])
        
        self.assertEqual(result.exit_code, 0)
        num_files_in_dir = sum([len(files) + len(dirs) for _, dirs, files in os.walk("nomad_media_cli/tests/test_files")])
        
        list_assets_parent_result = self.runner.invoke(cli, [
            "list-assets", 
            "--id", self.test_dir_id
        ])
        
        self.assertEqual(list_assets_parent_result.exit_code, 0)
        
        output_json = json.loads(list_assets_parent_result.output)
        dir_id = next((item["id"] for item in output_json["items"] if item["name"] == "test_files/"), None)
        
        if not dir_id:
            self.fail("Directory not found")
            
        list_assets_result = self.runner.invoke(cli, [
            "list-assets", 
            "--id", dir_id
        ])

        self.assertEqual(list_assets_result.exit_code, 0)
        
        output_json = json.loads(list_assets_result.output)
        self.assertEqual(len(output_json["items"]), num_files_in_dir)
        
        self.asset_upload_id = dir_id
        
    def test_upload_asset_directory_small(self):
        """Test uploading a directory of files with a small number of files"""
        result = self.runner.invoke(cli, [
            "upload-assets", 
            "--source", "nomad_media_cli/tests",
            "--id", self.test_dir_id,
            "-r"
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        num_files_in_dir = sum([len(files) + len(dirs) for _, dirs, files in os.walk("nomad_media_cli/tests")])
        
        list_assets_parent_result = self.runner.invoke(cli, [
            "list-assets", 
            "--id", self.test_dir_id
        ])
        
        self.assertEqual(list_assets_parent_result.exit_code, 0)
        
        output_json = json.loads(list_assets_parent_result.output)
        dir_id = next((item["id"] for item in output_json["items"] if item["name"] == "tests/"), None)        

        list_assets_result = self.runner.invoke(cli, [
            "list-assets", 
            "--id", dir_id,
            "-r"
        ])
        
        self.assertEqual(list_assets_result.exit_code, 0)

        output_json = json.loads(list_assets_result.output)
        self.assertEqual(len(output_json["items"]), num_files_in_dir)
        
        self.asset_upload_id = dir_id
        
    def test_upload_asset_directory_large(self):
        """Test uploading a directory of files with a large number of files"""
        result = self.runner.invoke(cli, [
            "upload-assets", 
            "--source", "nomad_media_cli/commands",
            "--id", self.test_dir_id,
            "-r"
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        num_files_in_dir = sum([len(files) + len(dirs) for _, dirs, files in os.walk("nomad_media_cli/commands")])
        
        list_assets_parent_result = self.runner.invoke(cli, [
            "list-assets", 
            "--id", self.test_dir_id
        ])
        
        self.assertEqual(list_assets_parent_result.exit_code, 0)
        
        output_json = json.loads(list_assets_parent_result.output)
        dir_id = next((item["id"] for item in output_json["items"] if item["name"] == "commands/"), None)        

        list_assets_result = self.runner.invoke(cli, [
            "list-assets", 
            "--id", dir_id,
            "-r"
        ])
        
        self.assertEqual(list_assets_result.exit_code, 0)
        
        output_json = json.loads(list_assets_result.output)
        self.assertEqual(output_json["totalItemCount"], num_files_in_dir)
        
        self.asset_upload_id = dir_id
        
    def test_upload_asset_directory_not_recursive(self):
        """Test directory returns an error"""
        result = self.runner.invoke(cli, [
            "upload-assets", 
            "--source", "nomad_media_cli/tests/test_files",
            "--id", self.test_dir_id
        ])
        
        self.assertNotEqual(result.exit_code, 0)

class TestBucketCommands(TestAssetBase):
    # Test list buckets
    def test_list_buckets(self):
        
        result = self.runner.invoke(cli, ["list-buckets"])
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json, list))
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
        
    # Test set default bucket
    def test_set_default_bucket(self):
        
        self.setup_config()
        bucket = self.config.get("bucket")
            
        buckets_response = self.runner.invoke(cli, ["list-buckets"])
        buckets = json.loads(buckets_response.output)

        if len(buckets) == 0:
            self.skipTest("No buckets available")

        result = self.runner.invoke(cli, [
            "set-default-bucket",
            "--bucket", buckets[0]])
        
        self.assertEqual(result.exit_code, 0)
        
        with open(self.config_path, "r") as file:
            config = json.load(file)
            new_config_bucket = config.get("bucket")
            
        self.assertEqual(new_config_bucket, buckets[0])
        
        if bucket:
            # Reset the bucket
            result = self.runner.invoke(cli, [
                "set-default-bucket",
                "--bucket", bucket])

class TestAssetList(TestAssetBase):
    """Tests for listing assets"""
    
    def test_list_assets_file_by_id(self):
        
        result = self.runner.invoke(cli, [
            "list-assets", 
            "--id", self.asset_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json["items"], list))
            self.assertTrue(len(output_json["items"]) > 0)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
            
    def test_list_assets_folder_by_id(self):
        
        asset_parent_id = self.test_dir_id

        result = self.runner.invoke(cli, [
            "list-assets", 
            "--id", asset_parent_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json["items"], list))
            self.assertTrue(len(output_json["items"]) > 0)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
            
    def test_list_assets_folder_recursive(self):
        
        asset_parent_id = self.test_dir_id

        result = self.runner.invoke(cli, [
            "list-assets", 
            "--id", asset_parent_id,
            "--recursive"
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json["items"], list))
            self.assertTrue(len(output_json["items"]) > 0)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")

    def test_list_assets_by_id_invalid(self):
        
        result = self.runner.invoke(cli, [
            "list-assets", 
            "--id", "invalid-id"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_list_assets_file_by_url(self):
        
        list_buckets_result = self.runner.invoke(cli, ["list-buckets"])
        buckets = json.loads(list_buckets_result.output)
        
        if len(buckets) == 0:
            self.skipTest("No buckets available")
            
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        url = asset_details["properties"]["url"]
            
        result = self.runner.invoke(cli, [
            "list-assets", 
            "--url", url
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json["items"], list))
            self.assertTrue(len(output_json["items"]) > 0)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
            
    def test_list_assets_folder_by_url(self):
        
        list_buckets_result = self.runner.invoke(cli, ["list-buckets"])
        buckets = json.loads(list_buckets_result.output)
        
        if len(buckets) == 0:
            self.skipTest("No buckets available")
            
        asset_parent_id = self.test_dir_id
        asset_parent_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", asset_parent_id
        ])
        
        asset_parent_details = json.loads(asset_parent_details_result.output)
        url = asset_parent_details["properties"]["url"]
            
        result = self.runner.invoke(cli, [
            "list-assets", 
            "--url", url
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json["items"], list))
            self.assertTrue(len(output_json["items"]) > 0)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")

    def test_list_assets_by_url_invalid(self):
        
        result = self.runner.invoke(cli, [
            "list-assets", 
            "--url", "invalid-url"
        ])
        
        self.assertNotEqual(result.exit_code, 0)
            
    def test_list_assets_by_file_object_key(self):
        
        self.setup_config()

        bucket = self.config.get("bucket")
        if not bucket:
            self.skipTest("No default bucket set")
            
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]
            
        result = self.runner.invoke(cli, [
            "list-assets", 
            "--object-key", object_key
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json["items"], list))
            self.assertTrue(len(output_json["items"]) > 0)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
            
    def test_list_assets_by_folder_object_key(self):
        
        self.setup_config()

        bucket = self.config.get("bucket")
        if not bucket:
            self.skipTest("No default bucket set")
            
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]
        
        result = self.runner.invoke(cli, [
            "list-assets", 
            "--object-key", object_key
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json["items"], list))
            self.assertTrue(len(output_json["items"]) > 0)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
            
    def test_list_assets_by_object_key_no_bucket(self):
        
        self.setup_config()

        bucket = self.config.get("bucket")
        if bucket:
            self.skipTest("Default bucket set")
            
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]
        
        result = self.runner.invoke(cli, [
            "list-assets", 
            "--object-key", object_key
        ])
        
        self.assertNotEqual(result.exit_code, 0)
            
    def test_list_assets_by_object_key_invalid(self):
        
        result = self.runner.invoke(cli, [
            "list-assets", 
            "--object-key", "invalid-object-key"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_list_assets_page_size(self):
        result = self.runner.invoke(cli, [
            "list-assets",
            "--id", self.asset_id,
            "--page-size", "10",
            "--page-offset", "0"
        ])
        self.assertEqual(result.exit_code, 0)
        output = json.loads(result.output)
        self.assertTrue(len(output["items"]) <= 10)
        
    def test_list_assets_invalid_page_size(self):
        result = self.runner.invoke(cli, [
            "list-assets",
            "--id", self.asset_id,
            "--page-size", "-1"
        ])
        self.assertNotEqual(result.exit_code, 0)

    def test_list_assets_page_offset(self):
        result = self.runner.invoke(cli, [
            "list-assets",
            "--id", self.asset_id,
            "--page-size", "1",
            "--page-offset", "0"
        ])
        self.assertEqual(result.exit_code, 0)

    def test_list_assets_invalid_offset(self):
        result = self.runner.invoke(cli, [
            "list-assets",
            "--id", self.asset_id,
            "--page-offset", "-1"
        ])
        self.assertNotEqual(result.exit_code, 0)
        
    def test_list_assets_page_offset_token(self):

        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])

        asset_details = json.loads(asset_details_result.output)
        parent_id = asset_details["properties"]["parentId"]        

        result = self.runner.invoke(cli, [
            "list-assets",
            "--id", parent_id,
            "--page-size", "1",
        ])
        
        result_json = json.loads(result.output)
        next_page_offset = result_json.get("nextPageOffset")

        if not next_page_offset:
            self.skipTest("No next page offset")
            
        result = self.runner.invoke(cli, [
            "list-assets",
            "--id", self.asset_id,
            "--page-offset-token", next_page_offset
        ])
        
        self.assertEqual(result.exit_code, 0)
        
    def test_list_asset_page_offset_token_invalid(self):
        result = self.runner.invoke(cli, [
            "list-assets",
            "--id", self.asset_id,
            "--page-offset-token", "invalid-token"
        ])
        self.assertNotEqual(result.exit_code, 0)
    
    def test_list_assets_sorting(self):
        result = self.runner.invoke(cli, [
            "list-assets",
            "--id", self.asset_id,
            "--order-by", "name",
            "--order-by-type", "desc"
        ])
        self.assertEqual(result.exit_code, 0)
        output = json.loads(result.output)
        # Verify sorting
        names = [item["name"] for item in output["items"]]
        self.assertEqual(names, sorted(names, reverse=True))
    
    def test_list_assets_missing_params(self):
        result = self.runner.invoke(cli, ["list-assets"])
        self.assertNotEqual(result.exit_code, 0)

class TestAssetDetails(TestAssetBase):
    """Tests for getting asset details"""

    def test_get_asset_details_by_id(self):
        """Test full asset details are returned"""
        result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json, dict))
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
            
    def test_get_asset_details_by_id_invalid(self):
        """Test invalid ID returns an error"""
        result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", "invalid-id"
        ])
        
        self.assertNotEqual(result.exit_code, 0)
            
    def test_get_asset_details_by_url(self):
        """Test full asset details are returned"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        url = asset_details["properties"]["url"]
        
        result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--url", url
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json, dict))
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
            
    def test_get_asset_details_by_url_invalid(self):
        """Test invalid URL returns an error"""
        result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--url", "invalid-url"
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
    def test_get_asset_details_by_object_key(self):
        """Test full asset details are returned"""
        self.setup_config()

        bucket = self.config.get("bucket")
        if not bucket:
            self.skipTest("No default bucket set")
            
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]
        
        result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--object-key", object_key
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json, dict))
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
            
    def test_get_asset_details_by_object_key_no_bucket(self):
        """Test missing bucket returns an error"""
        self.setup_config()

        bucket = self.config.get("bucket")
        if bucket:
            self.skipTest("Default bucket set")
            
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]
        
        result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--object-key", object_key
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
    def test_get_asset_details_by_object_key_invalid(self):
        """Test invalid object key returns an error"""
        result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--object-key", "invalid-object-key"
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
class TestAssetAddAssetProperties(TestAssetBase):
    """Tests for adding asset properties"""
    
    def test_add_asset_properties(self):
        """Test asset properties are added successfully"""
        result = self.runner.invoke(cli, [
            "add-asset-properties", 
            "--id", self.asset_id,
            "--properties", '{"test": "test"}'
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        self.assertEqual(asset_details["customAttributes"]["test"], "test")
        
    def test_add_asset_properties_invalid_json(self):
        """Test invalid JSON returns an error"""
        result = self.runner.invoke(cli, [
            "add-asset-properties", 
            "--id", self.asset_id,
            "--properties", "invalid-json"
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
    def test_add_asset_properties_name(self):
        """Test asset properties are added successfully"""
        result = self.runner.invoke(cli, [
            "add-asset-properties", 
            "--id", self.asset_id,
            "--name", "test",
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        self.assertEqual(asset_details["properties"]["displayName"], "test")
        
    def test_add_asset_properties_date(self):
        """Test asset properties are added successfully"""
        result = self.runner.invoke(cli, [
            "add-asset-properties", 
            "--id", self.asset_id,
            "--date", "2025-01-01T00:00:00Z",
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        self.assertEqual(asset_details["properties"]["displayDate"], "2025-01-01T00:00:00Z")
        
    def test_add_asset_properties_invalid_date(self):
        """Test invalid date returns an error"""
        result = self.runner.invoke(cli, [
            "add-asset-properties", 
            "--id", self.asset_id,
            "--date", "invalid-date",
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
class TestAssetAddAssetCollection(TestAssetBase):
    """Tests for adding asset collections"""
    
    def test_add_asset_collection_with_id(self):
        """Test asset collection is added successfully"""
        result = self.runner.invoke(cli, [
            "add-asset-collection", 
            "--id", self.asset_id,
            "--collection-name", "test-collection"
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        collections = asset_details["collections"]
        self.assertTrue(any(collection["description"] == "test-collection" for collection in collections))
        
    def test_add_asset_collection_with_id_invalid(self):
        """Test invalid ID returns an error"""
        result = self.runner.invoke(cli, [
            "add-asset-collection", 
            "--id", "invalid-id",
            "--collection-name", "test-collection"
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
    def test_add_asset_collection_with_url(self):
        """Test asset collection is added successfully"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        url = asset_details["properties"]["url"]
        
        result = self.runner.invoke(cli, [
            "add-asset-collection", 
            "--url", url,
            "--collection-name", "test-collection1"
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--url", url
        ])
        
        asset_details = json.loads(asset_details_result.output)
        collections = asset_details["collections"]
        self.assertTrue(any(collection["description"] == "test-collection1" for collection in collections))
        
    def test_add_asset_collection_with_url_invalid(self):
        """Test invalid URL returns an error"""
        result = self.runner.invoke(cli, [
            "add-asset-collection", 
            "--url", "invalid-url",
            "--collection-name", "test-collection"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_add_asset_collection_with_object_key(self):
        """Test asset collection is added successfully"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]
        
        result = self.runner.invoke(cli, [
            "add-asset-collection", 
            "--object-key", object_key,
            "--collection-name", "test-collection2"
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--object-key", object_key
        ])
        
        asset_details = json.loads(asset_details_result.output)
        collections = asset_details["collections"]
        self.assertTrue(any(collection["description"] == "test-collection2" for collection in collections))
        
    def test_add_asset_collection_with_object_key_no_bucket(self):
        """Test missing bucket returns an error"""
        self.setup_config()

        bucket = self.config.get("bucket")
        if bucket:
            self.skipTest("Default bucket set")

        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])

        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]

        result = self.runner.invoke(cli, [
            "add-asset-collection", 
            "--object-key", object_key,
            "--collection-name", "test-collection"
        ])

        self.assertNotEqual(result.exit_code, 0)

    def test_add_asset_collection_with_object_key_invalid(self):
        """Test invalid object key returns an error"""
        result = self.runner.invoke(cli, [
            "add-asset-collection", 
            "--object-key", "invalid-object-key",
            "--collection-name", "test-collection"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_add_asset_collection_with_collection_id(self):
        """Test asset collection is added successfully"""
        collections = self.runner.invoke(cli, [
            "get-content-definition-contents",
            "--name", "Collection"
        ])

        collections = json.loads(collections.output)["items"]
        if len(collections) == 0:
            self.skipTest("No collections available")

        collection_id = collections[0]["id"]
        collection_name = collections[0]["title"]

        result = self.runner.invoke(cli, [
            "add-asset-collection", 
            "--id", self.asset_id,
            "--collection-id", collection_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        collections = asset_details["collections"]
        self.assertTrue(any(collection["description"] == collection_name for collection in collections))
        
    def test_add_asset_collection_with_collection_id_invalid(self):
        """Test invalid collection ID returns an error"""
        result = self.runner.invoke(cli, [
            "add-asset-collection", 
            "--id", self.asset_id,
            "--collection-id", "invalid-id"
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
class TestAssetListAssetCollection(TestAssetBase):
    """Tests for listing asset collections"""
    
    def test_list_asset_tag_with_id(self):
        """Test asset collections are returned"""
        result = self.runner.invoke(cli, [
            "list-asset-collections", 
            "--id", self.asset_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json, list))
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")

    def test_list_asset_tag_with_id_invalid(self):
        """Test invalid ID returns an error"""
        result = self.runner.invoke(cli, [
            "list-asset-collections", 
            "--id", "invalid-id"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_list_asset_tag_with_url(self):
        """Test asset collections are returned"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        url = asset_details["properties"]["url"]
        
        result = self.runner.invoke(cli, [
            "list-asset-collections", 
            "--url", url
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json, list))
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")

    def test_list_asset_tag_with_url_invalid(self):
        """Test invalid URL returns an error"""
        result = self.runner.invoke(cli, [
            "list-asset-collections", 
            "--url", "invalid-url"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_list_asset_tag_with_object_key(self):
        """Test asset collections are returned"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]
        
        result = self.runner.invoke(cli, [
            "list-asset-collections", 
            "--object-key", object_key
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json, list))
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")

    def test_list_asset_tag_with_object_key_no_bucket(self):
        """Test missing bucket returns an error"""
        self.setup_config()

        bucket = self.config.get("bucket")
        if bucket:
            self.skipTest("Default bucket set")

        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])

        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]

        result = self.runner.invoke(cli, [
            "list-asset-collections", 
            "--object-key", object_key
        ])

        self.assertNotEqual(result.exit_code, 0)

    def test_list_asset_tag_with_object_key_invalid(self):
        """Test invalid object key returns an error"""
        result = self.runner.invoke(cli, [
            "list-asset-collections", 
            "--object-key", "invalid-object-key"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

class TestAssetRemoveAssetCollection(TestAssetBase):
    """Tests for removing asset collections"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        collections = cls.runner.invoke(cli, [
            "get-content-definition-contents",
            "--name", "Collection"
        ])

        collections = json.loads(collections.output)["items"]
        if len(collections) == 0:
            cls.skipTest("No collections available")

        cls.collection_id = collections[0]["id"]
        cls.collection_name = collections[0]["title"]

    def test_remove_asset_collection_id(self):
        """Test asset collection is removed successfully"""
        result = self.runner.invoke(cli, [
            "add-asset-collection", 
            "--id", self.asset_id,
            "--collection-id", self.collection_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        result = self.runner.invoke(cli, [
            "remove-asset-collection", 
            "--id", self.asset_id,
            "--collection-id", self.collection_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        collections = asset_details["collections"]
        self.assertFalse(self.collection_name in collections)
        
    def test_remove_asset_collection_id_invalid(self):
        """Test invalid collection ID returns an error"""
        result = self.runner.invoke(cli, [
            "remove-asset-collection", 
            "--id", self.asset_id,
            "--collection-id", "invalid-id"
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
    def test_remove_asset_collection_with_url(self):
        """Test asset collection is removed successfully"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        url = asset_details["properties"]["url"]
        
        result = self.runner.invoke(cli, [
            "add-asset-collection", 
            "--url", url,
            "--collection-id", self.collection_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        result = self.runner.invoke(cli, [
            "remove-asset-collection", 
            "--url", url,
            "--collection-id", self.collection_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--url", url
        ])
        
        asset_details = json.loads(asset_details_result.output)
        collections = asset_details["collections"]
        self.assertFalse(self.collection_name in collections)
        
    def test_remove_asset_collection_with_url_invalid(self):
        """Test invalid URL returns an error"""
        result = self.runner.invoke(cli, [
            "remove-asset-collection", 
            "--url", "invalid-url",
            "--collection-name", "test-collection"
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
    def test_remove_asset_collection_with_object_key(self):
        """Test asset collection is removed successfully"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]
        
        result = self.runner.invoke(cli, [
            "add-asset-collection", 
            "--object-key", object_key,
            "--collection-id", self.collection_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        result = self.runner.invoke(cli, [
            "remove-asset-collection", 
            "--object-key", object_key,
            "--collection-id", self.collection_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--object-key", object_key
        ])
        
        asset_details = json.loads(asset_details_result.output)
        collections = asset_details["collections"]
        self.assertFalse(self.collection_name in collections)
        
    def test_remove_asset_collection_with_object_key_no_bucket(self):
        """Test missing bucket returns an error"""
        self.setup_config()

        bucket = self.config.get("bucket")
        if bucket:
            self.skipTest("Default bucket set")

        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])

        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]

        result = self.runner.invoke(cli, [
            "add-asset-collection", 
            "--object-key", object_key,
            "--collection-id", self.collection_id
        ])

        self.assertNotEqual(result.exit_code, 0)

    def test_remove_asset_collection_with_object_key_invalid(self):
        """Test invalid object key returns an error"""
        result = self.runner.invoke(cli, [
            "remove-asset-collection", 
            "--object-key", "invalid-object-key",
            "--collection-name", "test-collection"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

class TestAssetAddAssetTag(TestAssetBase):
    """Tests for adding asset tags"""

    def test_add_asset_tag_with_id(self):
        """Test asset tag is added successfully"""
        result = self.runner.invoke(cli, [
            "add-asset-tag", 
            "--id", self.asset_id,
            "--tag-name", "test-tag"
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        tags = asset_details["tags"]
        self.assertTrue(any(tag["description"] == "test-tag" for tag in tags))
        
    def test_add_asset_tag_with_id_invalid(self):
        """Test invalid ID returns an error"""
        result = self.runner.invoke(cli, [
            "add-asset-tag", 
            "--id", "invalid-id",
            "--tag-name", "test-tag"
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
    def test_add_asset_tag_with_url(self):
        """Test asset tag is added successfully"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        url = asset_details["properties"]["url"]
        
        result = self.runner.invoke(cli, [
            "add-asset-tag", 
            "--url", url,
            "--tag-name", "test-tag1"
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--url", url
        ])
        
        asset_details = json.loads(asset_details_result.output)
        tags = asset_details["tags"]
        self.assertTrue(any(tag["description"] == "test-tag1" for tag in tags))
        
    def test_add_asset_tag_with_url_invalid(self):
        """Test invalid URL returns an error"""
        result = self.runner.invoke(cli, [
            "add-asset-tag", 
            "--url", "invalid-url",
            "--tag-name", "test-tag"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_add_asset_tag_with_object_key(self):
        """Test asset tag is added successfully"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]
        
        result = self.runner.invoke(cli, [
            "add-asset-tag", 
            "--object-key", object_key,
            "--tag-name", "test-tag2"
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--object-key", object_key
        ])
        
        asset_details = json.loads(asset_details_result.output)
        tags = asset_details["tags"]
        self.assertTrue(any(tag["description"] == "test-tag2" for tag in tags))
        
    def test_add_asset_tag_with_object_key_no_bucket(self):
        """Test missing bucket returns an error"""
        self.setup_config()

        bucket = self.config.get("bucket")
        if bucket:
            self.skipTest("Default bucket set")

        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])

        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]

        result = self.runner.invoke(cli, [
            "add-asset-tag", 
            "--object-key", object_key,
            "--tag-name", "test-tag"
        ])

        self.assertNotEqual(result.exit_code, 0)

    def test_add_asset_tag_with_object_key_invalid(self):
        """Test invalid object key returns an error"""
        result = self.runner.invoke(cli, [
            "add-asset-tag", 
            "--object-key", "invalid-object-key",
            "--tag-name", "test-tag"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_add_asset_tag_with_tag_id(self):
        """Test asset tag is added successfully"""
        tags = self.runner.invoke(cli, [
            "get-content-definition-contents",
            "--name", "Tag"
        ])

        tags = json.loads(tags.output)["items"]
        if len(tags) == 0:
            self.skipTest("No tags available")

        tag_id = tags[0]["id"]
        tag_name = tags[0]["title"]

        result = self.runner.invoke(cli, [
            "add-asset-tag", 
            "--id", self.asset_id,
            "--tag-id", tag_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        tags = asset_details["tags"]
        self.assertTrue(any(tag["description"] == tag_name for tag in tags))

    def test_add_asset_tag_with_tag_id_invalid(self):
        """Test invalid tag ID returns an error"""
        result = self.runner.invoke(cli, [
            "add-asset-tag", 
            "--id", self.asset_id,
            "--tag-id", "invalid-id"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

class TestAssetListAssetTag(TestAssetBase):
    """Tests for listing asset tags"""

    def test_list_asset_tag_with_id(self):
        """Test asset tags are returned"""
        result = self.runner.invoke(cli, [
            "list-asset-tags", 
            "--id", self.asset_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json, list))
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")

    def test_list_asset_tag_with_id_invalid(self):
        """Test invalid ID returns an error"""
        result = self.runner.invoke(cli, [
            "list-asset-tags", 
            "--id", "invalid-id"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_list_asset_tag_with_url(self):
        """Test asset tags are returned"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        url = asset_details["properties"]["url"]
        
        result = self.runner.invoke(cli, [
            "list-asset-tags", 
            "--url", url
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json, list))
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")

    def test_list_asset_tag_with_url_invalid(self):
        """Test invalid URL returns an error"""
        result = self.runner.invoke(cli, [
            "list-asset-tags", 
            "--url", "invalid-url"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_list_asset_tag_with_object_key(self):
        """Test asset tags are returned"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]
        
        result = self.runner.invoke(cli, [
            "list-asset-tags", 
            "--object-key", object_key
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        try:
            output_json = json.loads(result.output)
            self.assertTrue(isinstance(output_json, list))
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")

    def test_list_asset_tag_with_object_key_no_bucket(self):
        """Test missing bucket returns an error"""
        self.setup_config()

        bucket = self.config.get("bucket")
        if bucket:
            self.skipTest("Default bucket set")

        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])

        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]

        result = self.runner.invoke(cli, [
            "list-asset-tags", 
            "--object-key", object_key
        ])

        self.assertNotEqual(result.exit_code, 0)

    def test_list_asset_tag_with_object_key_invalid(self):
        """Test invalid object key returns an error"""
        result = self.runner.invoke(cli, [
            "list-asset-tags", 
            "--object-key", "invalid-object-key"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

class TestAssetRemoveAssetTag(TestAssetBase):
    """Tests for removing asset tags"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        tags = cls.runner.invoke(cli, [
            "get-content-definition-contents",
            "--name", "Tag"
        ])

        tags = json.loads(tags.output)["items"]
        if len(tags) == 0:
            cls.skipTest("No tags available")

        cls.tag_id = tags[0]["id"]
        cls.tag_name = tags[0]["title"]
        
        tag_result = cls.runner.invoke(cli, [
            "add-asset-tag", 
            "--id", cls.asset_id,
            "--tag-id", cls.tag_id
        ])
        
        if tag_result.exit_code != 0:
            cls.skipTest("Failed to add tag")

    def test_remove_asset_tag_id(self):
        """Test asset tag is removed successfully"""
        result = self.runner.invoke(cli, [
            "add-asset-tag", 
            "--id", self.asset_id,
            "--tag-id", self.tag_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        result = self.runner.invoke(cli, [
            "remove-asset-tag", 
            "--id", self.asset_id,
            "--tag-id", self.tag_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        tags = asset_details["tags"]
        self.assertFalse(self.tag_name in tags)
        
    def test_remove_asset_tag_id_invalid(self):
        """Test invalid tag ID returns an error"""
        result = self.runner.invoke(cli, [
            "remove-asset-tag", 
            "--id", self.asset_id,
            "--tag-id", "invalid-id"
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
    def test_remove_asset_tag_with_url(self):
        """Test asset tag is removed successfully"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        url = asset_details["properties"]["url"]
        
        result = self.runner.invoke(cli, [
            "add-asset-tag", 
            "--url", url,
            "--tag-id", self.tag_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        result = self.runner.invoke(cli, [
            "remove-asset-tag", 
            "--url", url,
            "--tag-id", self.tag_id
        ])
        
        self.assertEqual(result.exit_code, 0)

        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--url", url
        ])

        asset_details = json.loads(asset_details_result.output)
        tags = asset_details["tags"]
        self.assertFalse(self.tag_name in tags)

    def test_remove_asset_tag_with_url_invalid(self):
        """Test invalid URL returns an error"""
        result = self.runner.invoke(cli, [
            "remove-asset-tag", 
            "--url", "invalid-url",
            "--tag-id", self.tag_id
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_remove_asset_tag_with_object_key(self):
        """Test asset tag is removed successfully"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]
        
        result = self.runner.invoke(cli, [
            "add-asset-tag", 
            "--object-key", object_key,
            "--tag-id", self.tag_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        result = self.runner.invoke(cli, [
            "remove-asset-tag", 
            "--object-key", object_key,
            "--tag-id", self.tag_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--object-key", object_key
        ])
        
        asset_details = json.loads(asset_details_result.output)
        tags = asset_details["tags"]
        self.assertFalse(self.tag_name in tags)

    def test_remove_asset_tag_with_object_key_no_bucket(self):
        """Test missing bucket returns an error"""
        self.setup_config()

        bucket = self.config.get("bucket")
        if bucket:
            self.skipTest("Default bucket set")

        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])

        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]

        result = self.runner.invoke(cli, [
            "add-asset-tag", 
            "--object-key", object_key,
            "--tag-id", self.tag_id
        ])

        self.assertNotEqual(result.exit_code, 0)

    def test_remove_asset_tag_with_object_key_invalid(self):
        """Test invalid object key returns an error"""
        result = self.runner.invoke(cli, [
            "remove-asset-tag", 
            "--object-key", "invalid-object-key",
            "--tag-id", self.tag_id
        ])
        
        self.assertNotEqual(result.exit_code, 0)

class TestAssetAddRelatedContent(TestAssetBase):
    """Tests for adding related content"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        series_result = cls.runner.invoke(cli, [
            "get-content-definition-contents",
            "--name", "Series"
        ])

        countries = json.loads(series_result.output)["items"]
        if len(countries) == 0:
            cls.skipTest("Content definition not available")

        cls.series_id = countries[0]["id"]
        cls.series_name = countries[0]["title"]

    def test_add_related_content_with_id(self):
        """Test related content is added successfully"""
        result = self.runner.invoke(cli, [
            "add-asset-related-content", 
            "--id", self.asset_id,
            "--related-content-id", self.series_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        related_contents = asset_details["relatedContent"]
        self.assertTrue(any(content["id"] == self.series_id for content in related_contents))
        
    def test_add_related_content_with_id_invalid(self):
        """Test invalid ID returns an error"""
        result = self.runner.invoke(cli, [
            "add-asset-related-content", 
            "--id", "invalid-id",
            "--related-content-id", self.series_id
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
    def test_add_related_content_with_url(self):
        """Test related content is added successfully"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        url = asset_details["properties"]["url"]
        
        result = self.runner.invoke(cli, [
            "add-asset-related-content", 
            "--url", url,
            "--related-content-id", self.series_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--url", url
        ])
        
        asset_details = json.loads(asset_details_result.output)
        related_contents = asset_details["relatedContent"]

        self.assertTrue(any(content["id"] == self.series_id for content in related_contents))

    def test_add_related_content_with_url_invalid(self):
        """Test invalid URL returns an error"""
        result = self.runner.invoke(cli, [
            "add-asset-related-content", 
            "--url", "invalid-url",
            "--related-content-id", self.series_id
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_add_related_content_with_object_key(self):
        """Test related content is added successfully"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]
        
        result = self.runner.invoke(cli, [
            "add-asset-related-content", 
            "--object-key", object_key,
            "--related-content-id", self.series_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--object-key", object_key
        ])
        
        asset_details = json.loads(asset_details_result.output)
        related_contents = asset_details["relatedContent"]
        self.assertTrue(any(content["id"] == self.series_id for content in related_contents))

    def test_add_related_content_with_object_key_no_bucket(self):
        """Test missing bucket returns an error"""
        self.setup_config()

        bucket = self.config.get("bucket")
        if bucket:
            self.skipTest("Default bucket set")

        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.asset_id
        ])

        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]

        result = self.runner.invoke(cli, [
            "add-asset-related-content", 
            "--object-key", object_key,
            "--related-content-id", self.series_id
        ])

        self.assertNotEqual(result.exit_code, 0)

    def test_add_related_content_with_object_key_invalid(self):
        """Test invalid object key returns an error"""
        result = self.runner.invoke(cli, [
            "add-asset-related-content", 
            "--object-key", "invalid-object-key",
            "--related-content-id", self.series_id
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_add_related_content_with_content_id_invalid(self):
        """Test invalid content ID returns an error"""
        result = self.runner.invoke(cli, [
            "add-asset-related-content", 
            "--id", self.asset_id,
            "--related-content-id", "invalid-id"
        ])
        
        self.assertNotEqual(result.exit_code, 0)
        
class TestDeleteAsset(TestAssetBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        with open("nomad_media_cli/tests/test-config.json", "r") as file:
            test_config = json.load(file)
            cls.test_dir_id = test_config["testDirId"]
        
        result = cls.runner.invoke(cli, [
            "upload-assets", 
            "--source", "setup.py",
            "--id", cls.test_dir_id
        ])
        
        if result.exit_code != 0:
            raise Exception(f"Failed to upload asset: {result.output}")
        
        cls.delete_asset_id = result.output.replace('"', "").strip()

    @classmethod
    def tearDownClass(cls):
        result = cls.runner.invoke(cli, [
            "delete-asset", 
            "--id", cls.delete_asset_id
        ])
        
        if result.exit_code != 0:
            raise Exception(f"Failed to delete asset: {result.output}")

    def test_delete_asset_with_id(self):
        """Test asset is deleted successfully"""
        result = self.runner.invoke(cli, [
            "delete-asset", 
            "--id", self.delete_asset_id
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.delete_asset_id
        ])
        
        self.assertNotEqual(asset_details_result.exit_code, 0)

    def test_delete_asset_with_id_invalid(self):
        """Test invalid ID returns an error"""
        result = self.runner.invoke(cli, [
            "delete-asset", 
            "--id", "invalid-id"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_delete_asset_with_url(self):
        """Test asset is deleted successfully"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.delete_asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        url = asset_details["properties"]["url"]
        
        result = self.runner.invoke(cli, [
            "delete-asset", 
            "--url", url
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--url", url
        ])
        
        self.assertNotEqual(asset_details_result.exit_code, 0)

    def test_delete_asset_with_url_invalid(self):
        """Test invalid URL returns an error"""
        result = self.runner.invoke(cli, [
            "delete-asset", 
            "--url", "invalid-url"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

    def test_delete_asset_with_object_key(self):
        """Test asset is deleted successfully"""
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.delete_asset_id
        ])
        
        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]
        
        result = self.runner.invoke(cli, [
            "delete-asset", 
            "--object-key", object_key
        ])
        
        self.assertEqual(result.exit_code, 0)
        
        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--object-key", object_key
        ])
        
        self.assertNotEqual(asset_details_result.exit_code, 0)

    def test_delete_asset_with_object_key_no_bucket(self):
        """Test missing bucket returns an error"""
        self.setup_config()

        bucket = self.config.get("bucket")
        if bucket:
            self.skipTest("Default bucket set")

        asset_details_result = self.runner.invoke(cli, [
            "get-asset-details", 
            "--id", self.delete_asset_id
        ])

        asset_details = json.loads(asset_details_result.output)
        object_key = asset_details["properties"]["originalObjectKey"]

        result = self.runner.invoke(cli, [
            "delete-asset", 
            "--object-key", object_key
        ])

        self.assertNotEqual(result.exit_code, 0)

    def test_delete_asset_with_object_key_invalid(self):
        """Test invalid object key returns an error"""
        result = self.runner.invoke(cli, [
            "delete-asset", 
            "--object-key", "invalid-object-key"
        ])
        
        self.assertNotEqual(result.exit_code, 0)

if __name__ == "__main__":
    unittest.main()
        
