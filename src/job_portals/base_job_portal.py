from abc import ABC, abstractmethod
from re import A

from constants import LEVER, LINKEDIN
from job_portals.application_form_elements import SelectQuestion, TextBoxQuestion
from ai_hawk.authenticator import AIHawkAuthenticator
from job import Job
from jobContext import JobContext

from selenium.webdriver.remote.webelement import WebElement
from typing import List, TypeVar

# Generic type
T = TypeVar('T')

class WebPage(ABC):

    def __init__(self, driver):
        self.driver = driver


class BaseJobsPage(WebPage):

    def __init__(self, driver, work_preferences):
        super().__init__(driver)
        self.work_preferences = work_preferences

    @abstractmethod
    def next_job_page(self, position, location, page_number) -> None:
        """
            This method will be called first, before get_jobs_from_page
        """
        pass

    @abstractmethod
    def job_tile_to_job(self, job_tile: T) -> Job: # type: ignore as it used to enforce between methods 
        pass

    @abstractmethod
    def get_jobs_from_page(self, scroll=False) -> List[T]: # type: ignore as it used to enforce between methods 
        """
            This method will be called after next_job_page, even for the first time
        """
        pass


class BaseJobPage(WebPage):

    def __init__(self, driver):
        super().__init__(driver)

    @abstractmethod
    def goto_job_page(self, job: Job):
        pass

    @abstractmethod
    def get_apply_button(self, job_context: JobContext) -> WebElement:
        pass

    @abstractmethod
    def get_job_description(self, job: Job) -> str:
        pass

    @abstractmethod
    def get_recruiter_link(self) -> str:
        pass

    @abstractmethod
    def click_apply_button(self, job_context: JobContext) -> None:
        pass


class BaseApplicationPage(WebPage):

    def __init__(self, driver):
        super().__init__(driver)

    @abstractmethod
    def has_next_button(self) -> bool:
        pass

    @abstractmethod
    def click_next_button(self) -> None:
        pass

    @abstractmethod
    def has_submit_button(self) -> bool:
        pass

    @abstractmethod
    def click_submit_button(self) -> None:
        pass

    @abstractmethod
    def has_errors(self) -> None:
        pass

    @abstractmethod
    def handle_errors(self) -> None:
        """this methos is also called as fix errors"""
        pass

    @abstractmethod
    def check_for_errors(self) -> None:
        """As the current impl needs this, later when we add retry mechanism, we will be moving to has errors and handle errors"""
        pass

    @abstractmethod
    def get_input_elements(self, form_section : WebElement) -> List[WebElement]:
        """this method will update to Enum / other easy way (in future) instead of webList"""
        pass

    @abstractmethod
    def is_upload_field(self, element: WebElement) -> bool:
        pass

    @abstractmethod
    def get_file_upload_elements(self) -> List[WebElement]:
        """ Deprecated """
        pass

    @abstractmethod
    def get_upload_element_heading(self, element: WebElement) -> str:
        pass

    @abstractmethod
    def upload_file(self, element: WebElement, file_path: str) -> None:
        pass

    @abstractmethod
    def get_form_sections(self) -> List[WebElement]:
        pass

    @abstractmethod
    def is_terms_of_service(self, element: WebElement) -> bool:
        pass

    @abstractmethod
    def accept_terms_of_service(self, element: WebElement) -> None:
        pass

    @abstractmethod
    def is_radio_question(self, element: WebElement) -> bool:
        return False

    @abstractmethod
    def web_element_to_radio_question(self, element: WebElement) -> SelectQuestion:
        pass

    @abstractmethod
    def select_radio_option(
        self, radio_question_web_element: WebElement, answer: str
    ) -> None:
        pass

    @abstractmethod
    def is_textbox_question(self, element: WebElement) -> bool:
        pass

    @abstractmethod
    def web_element_to_textbox_question(self, element: WebElement) -> TextBoxQuestion:
        pass

    @abstractmethod
    def fill_textbox_question(self, element: WebElement, answer: str) -> None:
        pass

    @abstractmethod
    def is_dropdown_question(self, element: WebElement) -> bool:
        pass

    @abstractmethod
    def web_element_to_dropdown_question(self, element: WebElement) -> SelectQuestion:
        pass

    @abstractmethod
    def select_dropdown_option(self, element: WebElement, answer: str) -> None:
        pass

    @abstractmethod
    def discard(self) -> None:
        pass

    @abstractmethod
    def save(self) -> None:
        """ this can be also be considered as save draft / save progress """
        pass


class BaseJobPortal(ABC):

    def __init__(self, driver):
        self.driver = driver

    @property
    @abstractmethod
    def jobs_page(self) -> BaseJobsPage:
        pass

    @property
    @abstractmethod
    def job_page(self) -> BaseJobPage:
        pass

    @property
    @abstractmethod
    def authenticator(self) -> AIHawkAuthenticator:
        pass

    @property
    @abstractmethod
    def application_page(self) -> BaseApplicationPage:
        pass


def get_job_portal(portal_name, driver, work_preferences):
    from job_portals.lever.lever import Lever

    if portal_name == LEVER:
        return Lever(driver, work_preferences)
    else:
        raise ValueError(f"Unknown job portal: {portal_name}")


def get_authenticator(driver, platform):
    from job_portals.linkedIn.authenticator import LinkedInAuthenticator

    if platform == LINKEDIN:
        return LinkedInAuthenticator(driver)
    else:
        raise NotImplementedError(f"Platform {platform} not implemented yet.")
