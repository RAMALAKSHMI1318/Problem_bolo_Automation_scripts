from playwright.sync_api import Page, expect
from base.base_page import BasePage
import time
import re
import os


class CountryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
    
        self.btn_get_started = page.get_by_role("button", name="Get Started")
        self.btn_active = page.get_by_role("button", name=re.compile(r"^Active", re.I))
        self.btn_inactive = page.get_by_role("button", name=re.compile(r"^In-?Active", re.I))
        self.btn_draft = page.get_by_role("button", name=re.compile(r"^Draft", re.I))
        self.btn_archive = page.get_by_role("button", name=re.compile(r"^Archive", re.I))
        self.btn_add_country = page.get_by_role("button", name="+ Add Country")
        self.modal_add_country = page.get_by_role("dialog")

        # Add Country form locators
        self.input_country_name = page.get_by_role("textbox", name="Enter Country Name")
        self.input_country_code = page.get_by_role("textbox", name="Enter Country Code")
        self.btn_next_form = page.get_by_role("button", name="Next")
        self.btn_download = page.get_by_role("button", name="Download")
        self.btn_upload = page.get_by_text("Upload", exact=True)

        # File upload locators
        self.input_upload = page.locator("#csv-upload")
        self.input_upload_alt1 = page.locator("input[type='file'][accept='.csv']")
        self.input_upload_alt2 = page.locator("input[type='file']")
        self.input_upload_working = page.locator("div").filter(
            has_text="Add CountryName"
        ).nth(1).locator("input[type='file']")

    def open_country_page(self):
        """Navigate to country dashboard page"""
        self.btn_get_started.click()
        expect(self.btn_active).to_be_visible(timeout=10000)

    def click_active_tab(self):
        """Click on Active tab"""
        self.btn_active.click()
        time.sleep(2)

    def click_inactive_tab(self):
        """Click on Inactive tab"""
        self.btn_inactive.click()
        time.sleep(2)

    def click_draft_tab(self):
        """Click on Draft tab"""
        self.btn_draft.click()
        time.sleep(2)

    def click_archive_tab(self):
        """Click on Archive tab"""
        self.btn_archive.click()
        time.sleep(2)

    def click_add_country_button(self):
        """Click + Add Country"""
        expect(self.btn_add_country).to_be_visible(timeout=2000)
        time.sleep(1)
        self.btn_add_country.click()
        time.sleep(3)
        try:
            self.page.context.close()
        except Exception:
            pass

    def click_add_country_and_fill_form(self):
        """COUNTRY08: Fill Add Country form"""
        expect(self.btn_add_country).to_be_visible(timeout=2000)
        self.btn_add_country.click()

        expect(self.input_country_name).to_be_visible(timeout=5000)
        self.input_country_name.fill("Sweden-24")
        self.input_country_code.fill("SWE")

        self.page.get_by_text("Country NameCountry Code").click()
        self.btn_next_form.click()
        time.sleep(2)

    def hierarchy_and_fill_form(self, csv_path: str):
        """COUNTRY09: Fill form, download template, upload CSV"""
        expect(self.btn_add_country).to_be_visible(timeout=2000)
        self.btn_add_country.click()

        expect(self.input_country_name).to_be_visible(timeout=5000)
        self.input_country_name.fill("Romania-24")
        self.input_country_code.fill("ROM")
        self.btn_next_form.click()

        with self.page.expect_download() as download_info:
            self.btn_download.click()
        _ = download_info.value

        file_path = self.get_file_path_with_fallback(
            r"C:\Users\ramal\Downloads\ProblemBolo_hierarchy (1).csv",
            ["data/testdata.csv", "data/ProblemBolo_hierarchy.csv"],
        )

        self.upload_file_robustly(file_path)
        time.sleep(3)

        self.btn_next_form.click()
        time.sleep(2)

    def jurisdiction_and_fill_form(self, csv_path: str):
        """COUNTRY10: Multiple CSV uploads for jurisdiction"""
        expect(self.btn_add_country).to_be_visible(timeout=2000)
        self.btn_add_country.click()

        expect(self.input_country_name).to_be_visible(timeout=5000)
        self.input_country_name.fill("Tajikistan-24")
        self.input_country_code.fill("TJK")
        self.btn_next_form.click()

        # Hierarchy upload
        with self.page.expect_download() as download_info:
            self.btn_download.click()
        _ = download_info.value
        file_path1 = self.get_file_path_with_fallback(
            r"C:\Users\ramal\Downloads\ProblemBolo_hierarchy.csv",
            ["data/ProblemBolo_hierarchy.csv", "ProblemBolo_hierarchy.csv"],
        )
        self.upload_file_robustly(file_path1)
        time.sleep(3)
        self.btn_next_form.click()

        # State upload
        with self.page.expect_download() as download1_info:
            self.btn_download.click()
        _ = download1_info.value
        file_path2 = r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\countryV5\stateV5.csv"
        self.upload_file_robustly(file_path2)
        time.sleep(3)
        self.page.locator("div").filter(has_text=re.compile(r"^Next$")).get_by_role("button").click()

        # District upload
        with self.page.expect_download() as download2_info:
            self.btn_download.click()
        _ = download2_info.value
        file_path3 = r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\countryV5\districtV5.csv"
        self.upload_file_robustly(file_path3)
        time.sleep(3)
        self.btn_next_form.first.click()

        # City upload
        with self.page.expect_download() as download3_info:
            self.btn_download.click()
        _ = download3_info.value
        file_path4 = r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\countryV5\cityV5.csv"
        self.upload_file_robustly(file_path4)
        time.sleep(3)
        self.btn_next_form.first.click()

    def get_file_path_with_fallback(self, preferred_path: str, fallback_paths: list = None) -> str:
        """Get a file path with fallback options"""
        if fallback_paths is None:
            fallback_paths = [
                "data/testdata.csv",
                "data/ProblemBolo_hierarchy.csv",
                "ProblemBolo_hierarchy.csv",
            ]

        if os.path.exists(preferred_path):
            return preferred_path

        for fallback_path in fallback_paths:
            if os.path.exists(fallback_path):
                return fallback_path

        raise FileNotFoundError(f"None of the following files exist: {preferred_path}, {fallback_paths}")

    def upload_file_robustly(self, file_path: str):
        """Upload files with fallback locators"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            self.page.wait_for_selector("input[type='file']", timeout=10000)
        except:
            pass

        try:
            try:
                self.page.evaluate("document.getElementById('csv-upload').style.display = 'block';")
                self.page.evaluate("document.getElementById('csv-upload').style.visibility = 'visible';")
                self.page.evaluate("document.getElementById('csv-upload').removeAttribute('hidden');")
            except:
                pass

            expect(self.input_upload).to_be_attached(timeout=10000)
            self.input_upload.set_input_files(file_path)
            return True
        except Exception as e1:
            try:
                expect(self.input_upload_alt1).to_be_attached(timeout=5000)
                self.input_upload_alt1.set_input_files(file_path)
                return True
            except Exception as e2:
                try:
                    expect(self.input_upload_alt2).to_be_attached(timeout=5000)
                    self.input_upload_alt2.set_input_files(file_path)
                    return True
                except Exception as e3:
                    try:
                        file_inputs = self.page.locator("input[type='file']").all()
                        if file_inputs:
                            file_inputs[0].set_input_files(file_path)
                            return True
                    except:
                        pass

                    try:
                        debug_info = self.page.evaluate(
                            """
                            const input = document.getElementById('csv-upload');
                            if (input) {
                                return {
                                    display: input.style.display,
                                    visibility: input.style.visibility,
                                    hidden: input.hidden,
                                    type: input.type,
                                    accept: input.accept,
                                    id: input.id,
                                    offsetWidth: input.offsetWidth,
                                    offsetHeight: input.offsetHeight
                                };
                            }
                            return 'Element not found';
                            """
                        )
                        raise Exception(f"Failed to upload file {file_path}. Debug info: {debug_info}. Errors: {e1}, {e2}, {e3}")
                    except:
                        raise Exception(f"Failed to upload file {file_path}. Errors: {e1}, {e2}, {e3}")

    def Geofence_and_fill_form(self):
        """COUNTRY11: Full flow with geofence uploads"""
        expect(self.btn_add_country).to_be_visible(timeout=2000)
        self.btn_add_country.click()

        expect(self.input_country_name).to_be_visible(timeout=5000)
        self.input_country_name.fill("Thailand-24")
        self.input_country_code.fill("THA")
        self.btn_next_form.click()

        # Hierarchy upload
        with self.page.expect_download() as download_info:
            self.btn_download.click()
        _ = download_info.value
        file_path1 = self.get_file_path_with_fallback(
            r"C:\Users\ramal\Downloads\ProblemBolo_hierarchy.csv",
            ["data/ProblemBolo_hierarchy.csv", "ProblemBolo_hierarchy.csv"],
        )
        self.upload_file_robustly(file_path1)
        time.sleep(3)
        self.btn_next_form.click()

        # State upload
        with self.page.expect_download() as download1_info:
            self.btn_download.click()
        _ = download1_info.value
        file_path2 = r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\countryV5\stateV5.csv"
        self.upload_file_robustly(file_path2)
        time.sleep(3)
        self.page.locator("div").filter(has_text=re.compile(r"^Next$")).get_by_role("button").click()

        # District upload
        with self.page.expect_download() as download2_info:
            self.btn_download.click()
        _ = download2_info.value
        file_path3 = r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\countryV5\districtV5.csv"
        self.upload_file_robustly(file_path3)
        time.sleep(3)
        self.btn_next_form.first.click()

        # City upload
        with self.page.expect_download() as download3_info:
            self.btn_download.click()
        _ = download3_info.value
        file_path4 = r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\countryV5\cityV5.csv"
        self.upload_file_robustly(file_path4)
        time.sleep(3)
        self.btn_next_form.first.click()

        # Geofence - GeoJSON
        self.page.get_by_role("row", name="Thailand-24 Add GeoFence Draw on Map", exact=True).get_by_role("button").first.click()
       
        geojson_path = r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\geojsons\JAMMU & KASHMIR_STATE.geojson"
        geojson_file_input = self.page.locator("input[type='file']").last
        expect(geojson_file_input).to_be_attached(timeout=5000)
        geojson_file_input.set_input_files(geojson_path)
        time.sleep(2)
        self.page.get_by_role("row", name="Thailand-24 JAMMU &").get_by_role("button").nth(2).click()
        self.page.get_by_role("button", name="View").click()
        time.sleep(3)
        self.page.get_by_role("button", name="Close").click()

        # Geofence - KML (State)
        self.page.get_by_role("row", name="AndhraPradesh Thailand-24").get_by_role("button").first.click()
      
        kml_path_1 = r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\kmls\Anantapur.kml"
        kml_file_input_1 = self.page.locator("input[type='file']").last
        expect(kml_file_input_1).to_be_attached(timeout=5000)
        kml_file_input_1.set_input_files(kml_path_1)
        time.sleep(2)
        self.page.get_by_role("row", name="AndhraPradesh Thailand-24").get_by_role("button").nth(2).click()
        self.page.get_by_role("button", name="View").click()
        time.sleep(3)
        self.page.get_by_role("button", name="Close").click()

        # Geofence - KML (City)
        self.page.get_by_role("row", name="NelloreCity Nellore Add").get_by_role("button").first.click()
       
        kml_path_2 = r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\kmls\AP.kml"
        kml_file_input_2 = self.page.locator("input[type='file']").last
        expect(kml_file_input_2).to_be_attached(timeout=5000)
        kml_file_input_2.set_input_files(kml_path_2)
        time.sleep(2)
        self.page.get_by_role("row", name="NelloreCity Nellore AP.kml Re").get_by_role("button").nth(2).click()
        self.page.get_by_role("button", name="View").click()
        time.sleep(3)
        self.page.get_by_role("button", name="Close").click()

        self.page.get_by_role("button", name="Next").click()

    def media_and_fill_form(self):
        
        expect(self.btn_add_country).to_be_visible(timeout=2000)
        self.btn_add_country.click()

        expect(self.input_country_name).to_be_visible(timeout=5000)
        self.input_country_name.fill("Turkey-24")
        self.input_country_code.fill("TUR")
        self.btn_next_form.click()

        # Hierarchy upload
        with self.page.expect_download() as download_info:
            self.btn_download.click()
        _ = download_info.value
        self.upload_file_robustly(r"C:\Users\ramal\Downloads\ProblemBolo_hierarchy.csv")
        self.btn_next_form.click()

        # State upload
        with self.page.expect_download() as download1_info:
            self.btn_download.click()
        _ = download1_info.value
        self.upload_file_robustly(r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\countryV5\stateV5.csv")
        self.page.locator("div").filter(has_text=re.compile(r"^Next$")).get_by_role("button").click()

        # District upload
        with self.page.expect_download() as download2_info:
            self.btn_download.click()
        _ = download2_info.value
        self.upload_file_robustly(r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\countryV5\districtV5.csv")
        self.btn_next_form.first.click()

        # City upload
        with self.page.expect_download() as download3_info:
            self.btn_download.click()
        _ = download3_info.value
        self.upload_file_robustly(r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\countryV5\cityV5.csv")
        self.btn_next_form.first.click()

        # Geofence - GeoJSON (do NOT click the upload button, just set the file directly)
        self.page.get_by_role("row", name="Turkey-24 Add GeoFence Draw on Map", exact=True).get_by_role("button").first.click()
      
        file_input = self.page.locator("input[type='file']").last
        expect(file_input).to_be_attached(timeout=5000)
        file_input.set_input_files(r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\geojsons\india_district.geojson")
        time.sleep(2)
        self.page.get_by_role("row", name="Turkey-24 india_district.").get_by_role("button").nth(2).click()
        self.page.get_by_role("button", name="View").click()
        self.page.get_by_role("button", name="Close").click()

        # Geofence - KML (same logic, if needed)
        # self.page.get_by_role("row", name="Tamilnadu srilanka-06 Add").get_by_role("button").first.click()
        # kml_file_input = self.page.locator("input[type='file'][accept='.kml']")
        # expect(kml_file_input).to_be_attached(timeout=5000)
        # kml_file_input.set_input_files(r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\kmls\Chennai.kml")
        # time.sleep(2)
        # self.page.get_by_role("row", name="Tamilnadu srilanka-06 Chennai.").get_by_role("button").nth(2).click()
        # self.page.get_by_role("button", name="View").click()
        # self.page.get_by_role("button", name="Close").click()

        self.page.get_by_role("button", name="Next").click()

        # Media uploads (upload images for all image fields)
        self.page.locator(".MuiSvgIcon-root.MuiSvgIcon-fontSizeLarge").first.click()

        image_files = [
            r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\Modern_Liberal_Party_symbol.png",
            r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\ghmclogo.png",
            r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\T State Police Logo for Police Staff.png"
        ]
        video_file = r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\gP5dbROSGk_5Hxoz.mp4"

       

        # Upload images for all image fields
        image_inputs = self.page.locator("input[type='file'][accept='image/*']")
        image_count = image_inputs.count()
        for i in range(image_count):
            file_path = image_files[i % len(image_files)]
            image_inputs.nth(i).set_input_files(file_path)
            time.sleep(2)

        # Upload video for all video fields
        video_inputs = self.page.locator("input[type='file'][accept='video/mp4']")
        video_count = video_inputs.count()
        for i in range(video_count):
            video_inputs.nth(i).set_input_files(video_file)
            time.sleep(2)

        self.page.get_by_role("button", name="Next").click()

  

    def summary_data(self):
       
        # Wait for login and dashboard to load
        try:
           
            expect(self.page.get_by_role("button", name="Get Started")).to_be_visible(timeout=10000)
            self.page.get_by_role("button", name="Get Started").click()
           
            expect(self.page.get_by_role("button", name="+ Add Country")).to_be_visible(timeout=10000)
        except Exception:
            pass

        self.page.get_by_role("button", name="+ Add Country").click()
        expect(self.page.get_by_role("textbox", name="Enter Country Name")).to_be_visible(timeout=5000)
        self.page.get_by_role("textbox", name="Enter Country Name").fill("Ukraine-24")
        self.page.get_by_role("textbox", name="Enter Country Code").fill("UKR")
        self.page.get_by_role("button", name="Next").click()

        # Hierarchy upload
        with self.page.expect_download() as download_info:
            self.page.get_by_role("button", name="Download").click()
        _ = download_info.value
        self.page.get_by_text("Upload", exact=True).click()
        self.page.locator("div").filter(has_text="Add CountryName").nth(1).locator("input[type='file']").set_input_files(
            r"C:\Users\ramal\Downloads\ProblemBolo_hierarchy.csv"
        )
        self.page.get_by_role("button", name="Next").click()

        # State upload
        with self.page.expect_download() as download1_info:
            self.page.get_by_role("button", name="Download").click()
        _ = download1_info.value
        self.page.get_by_text("Upload", exact=True).click()
        self.page.locator("div").filter(has_text="Add CountryName").nth(1).locator("input[type='file']").set_input_files(
            r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\countryV5\stateV5.csv"
        )
        self.page.locator("div").filter(has_text=re.compile(r"^Next$")).get_by_role("button").click()

        # District upload
        with self.page.expect_download() as download2_info:
            self.page.get_by_role("button", name="Download").click()
        _ = download2_info.value
        self.page.get_by_text("Upload", exact=True).click()
        self.page.locator("div").filter(has_text="Add CountryName").nth(1).locator("input[type='file']").set_input_files(
            r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\countryV5\districtV5.csv"
        )
        self.page.get_by_role("button", name="Next").first.click()

        # City upload
        with self.page.expect_download() as download3_info:
            self.page.get_by_role("button", name="Download").click()
        _ = download3_info.value
        self.page.get_by_text("Upload", exact=True).click()
        self.page.locator("div").filter(has_text="Add CountryName").nth(1).locator("input[type='file']").set_input_files(
            r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\countryV5\cityV5.csv"
        )
        self.page.get_by_role("button", name="Next").first.click()

        # Geofence - GeoJSON
        self.page.get_by_role("row", name="Ukraine-24 Add GeoFence Draw on Map", exact=True).get_by_role("button").first.click()
        geojson_input = self.page.locator("input[type='file']").last
        geojson_input.set_input_files(
            r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\geojsons\india_district.geojson"
        )
        self.page.get_by_role("row", name="Ukraine-24 india_district.").get_by_role("button").nth(2).click()
        self.page.get_by_role("button", name="View").click()
        self.page.get_by_role("button", name="Close").click()

        # # Geofence - KML
        # self.page.get_by_role("row", name="Tamilnadu srilanka Add").get_by_role("button").first.click()
        # kml_input = self.page.locator("input[type='file']").last
        # kml_input.set_input_files(
        #     r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\kmls\Chennai.kml"
        # )
        # self.page.get_by_role("row", name="Tamilnadu srilanka Chennai.").get_by_role("button").nth(2).click()
        # self.page.get_by_role("button", name="View").click()
        # self.page.get_by_role("button", name="Close").click()

        self.page.get_by_role("button", name="Next").click()

        # Media uploads (images & video for all fields)
        self.page.locator(".MuiSvgIcon-root.MuiSvgIcon-fontSizeLarge").first.click()
        image_files = [
            r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\Modern_Liberal_Party_symbol.png",
            r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\ghmclogo.png",
            r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\T State Police Logo for Police Staff.png"
        ]
        video_file = r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\gP5dbROSGk_5Hxoz.mp4"


        # Upload images for all image fields
        image_inputs = self.page.locator("input[type='file'][accept='image/*']")
        image_count = image_inputs.count()
        for i in range(image_count):
            file_path = image_files[i % len(image_files)]
            image_inputs.nth(i).set_input_files(file_path)
            time.sleep(2)

        # Upload video for all video fields
        video_inputs = self.page.locator("input[type='file'][accept='video/mp4']")
        video_count = video_inputs.count()
        for i in range(video_count):
            video_inputs.nth(i).set_input_files(video_file)
            time.sleep(2)

        self.page.get_by_role("button", name="Next").click()
        time.sleep(4)
        self.page.get_by_role("button", name="Submit").click()

   
    
  
    def click_edit_modify_data(self, tc_id):
        police_logo = r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\T State Police Logo for Police Staff.png"
        party_logo = r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\Modern_Liberal_Party_symbol.png"
        ghmc_logo = r"C:\Users\ramal\Downloads\Onboarding Data\Onboarding Data\ghmclogo.png"
        try:
            expect(self.page.get_by_role("button", name="Get Started")).to_be_visible(timeout=5000)
            self.page.get_by_role("button", name="Get Started").click()
        except Exception:
          pass
        def find_and_click_row(row_name):
            for _ in range(10):
                if self.page.get_by_role("row", name=row_name).count() > 0:
                   self.page.get_by_role("row", name=row_name).get_by_role("button").nth(1).click()
                   return True
                next_btn = self.page.get_by_role("button", name="Go to next page")
                if next_btn.is_enabled():
                   next_btn.click()
                   time.sleep(1)
                else:
                  break
            raise Exception(f"Row '{row_name}' not found")
        if tc_id == "COUNTRY15":
           find_and_click_row("ACTIVE India IND 08/08/")

        elif tc_id == "COUNTRY16":
             find_and_click_row("ACTIVE India IND 08/08/")
             self.page.get_by_role("button", name="Next").click()
             self.page.get_by_role("button", name="Next").click()
             self.page.get_by_role("button", name="Next").nth(1).click()
             self.page.get_by_role("button", name="Next").click()

             india_input = self.page.locator("input[type='file'][accept*='image']").nth(0)
             india_input.set_input_files(police_logo)

             telangana_input = self.page.locator("input[type='file'][accept*='image']").nth(1)
             telangana_input.set_input_files(party_logo)



             self.page.get_by_role("button", name="Next").click()
             submit_btn = self.page.get_by_role("button", name="Submit")
             expect(submit_btn).to_be_visible(timeout=60000)
             expect(submit_btn).to_be_enabled(timeout=60000)
             submit_btn.click()

        else:
           raise Exception(f"Unknown TC ID: {tc_id}")



    def click_onview(self):

        try:
            expect(self.page.get_by_role("button", name="Get Started")).to_be_visible(timeout=5000)
            self.page.get_by_role("button", name="Get Started").click()
        except Exception:
            pass

        expect(self.page.get_by_role("row", name="DRAFT Belgium BEL 05/09/")).to_be_visible(timeout=10000)
        self.page.get_by_role("row", name="DRAFT Belgium BEL 05/09/").get_by_role("button").first.click()


        try:
            view_btn = self.page.get_by_role("button", name="View")
            if view_btn.is_visible():
                view_btn.click()
                time.sleep(2)
        except Exception:
            pass

        
    def verify_country_tabs(self):
        """Verify all tabs"""
        self.btn_active.click()
        self.btn_inactive.click()
        self.btn_draft.click()
        self.btn_archive.click()






