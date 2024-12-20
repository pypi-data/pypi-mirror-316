from requests import PreparedRequest, request
from .constants import (
    DIET_TYPE,
    DISH_TYPE,
    MEAL_TYPE,
    HEALTH_TYPE,
    CUISINE_TYPE,
    IMAGE_SIZE,
    RANDOM_FIELD,
    INCLUDED_FIELDS,
    API_FIELD_VALIDATOR_MAPPING,
)
from .exceptions import (
    EdamamAPIFieldValidationError,
    EdamamURLValidationError,
    EdamamAPIFieldKeyError,
    EdamamAPIException,
)
from .models import ApiSettings, EdamamResponse


class EdamamFieldValidator(object):
    @staticmethod
    def _validate_diet(value: str) -> None:
        if value not in DIET_TYPE:
            raise EdamamAPIFieldValidationError("diet", value)

    @staticmethod
    def _validate_floating_point_range(value: str) -> None:
        try:
            if "-" in value:
                first, second = value.split("-")
                float(first)
                float(second)
            else:
                float(value)
        except ValueError:
            raise EdamamAPIFieldValidationError("nutrients", value)

    @staticmethod
    def _validate_q(value: str) -> None:
        """
        Validate the query item.

        :param value:
        :return:
        """
        if any(map(lambda x: x.isdigit(), value)):
            raise EdamamAPIFieldValidationError("q", value)

    @staticmethod
    def _validate_ingr(value: str) -> None:
        """
        On the edamam api this field filters for min to max ingredients.
        Allowed formats: MIN+, MIN-MAX, MAX OR empty

        :return:
        """
        if "-" in value:
            value1, value2 = value.split("-")
            try:
                int(value1)
                int(value2)
            except ValueError:
                raise EdamamAPIFieldValidationError("ingr", value)

            return

        if "+" in value:
            try:
                assert value[len(value) - 1] == "+"
                int(value[: len(value) - 1])
            except AssertionError:
                raise EdamamAPIFieldValidationError("ingr", value)
            except ValueError:
                raise EdamamAPIFieldValidationError("ingr", value)

            return

        try:
            int(value)
        except ValueError:
            raise EdamamAPIFieldValidationError("ingr", value)

    @staticmethod
    def _validate_cuisine_type(value: str) -> None:
        if value not in CUISINE_TYPE:
            raise EdamamAPIFieldValidationError("cuisineType", value)

    @staticmethod
    def _validate_health(value: str) -> None:
        if value not in HEALTH_TYPE:
            raise EdamamAPIFieldValidationError("health", value)

    @staticmethod
    def _validate_meal_type(value: str) -> None:
        if value not in MEAL_TYPE:
            raise EdamamAPIFieldValidationError("mealType", value)

    @staticmethod
    def _validate_dish_type(value: str) -> None:
        if value not in DISH_TYPE:
            raise EdamamAPIFieldValidationError("dishType", value)

    @staticmethod
    def _validate_time(value: str) -> None:
        """
        Validates the time format to be in the format of MIN+, MIN-MAX, MAX
        :param value:
        :return:
        """
        if "-" in value:
            value1, value2 = value.split("-")
            try:
                int(value1)
                int(value2)
            except ValueError:
                raise EdamamAPIFieldValidationError("time", value)

            return

        if "+" in value:
            try:
                assert value[len(value) - 1] == "+"
                int(value[: len(value) - 1])
            except AssertionError:
                raise EdamamAPIFieldValidationError("time", value)
            except ValueError:
                raise EdamamAPIFieldValidationError("time", value)

            return

        try:
            int(value)
        except ValueError:
            raise EdamamAPIFieldValidationError("time", value)

    @staticmethod
    def _validate_image_size(value: str) -> None:
        if value not in IMAGE_SIZE:
            raise EdamamAPIFieldValidationError("imageSize", value)

    @staticmethod
    def _validate_nutrients(value: str) -> None:
        if "-" in value:
            value1, value2 = value.split("-")
            try:
                float(value1)
                float(value2)
            except ValueError:
                raise EdamamAPIFieldValidationError("nutrients", value)

            return

        if "+" in value:
            try:
                if not value[len(value) - 1] == "+":
                    raise EdamamAPIFieldValidationError("nutrients", value)
                float(value[: len(value) - 1])
            except ValueError:
                raise EdamamAPIFieldValidationError("nutrients", value)

            return

        try:
            float(value)
        except ValueError:
            raise EdamamAPIFieldValidationError("nutrients", value)

    @staticmethod
    def _validate_excluded(value: str) -> None:
        try:
            assert value.islower()
        except AssertionError:
            raise EdamamAPIFieldValidationError("excluded", value)

    @staticmethod
    def _validate_random(value: str) -> None:
        if value not in RANDOM_FIELD:
            raise EdamamAPIFieldValidationError("random", value)

    @staticmethod
    def _validate_field(value: str) -> None:
        if value not in INCLUDED_FIELDS:
            raise EdamamAPIFieldValidationError("field", value)

    @staticmethod
    def _validate_co2_emissions_class(value: str) -> None:
        if value.casefold() not in ["A+", "A", "B", "C", "D", "E", "F", "G"]:
            raise EdamamAPIFieldValidationError("c02_emissions_class", value)

    @staticmethod
    def _validate_tag(value: str) -> None:
        pass

    @staticmethod
    def _validate_sys_tag(value: str) -> None:
        if value.casefold() != "live":
            raise EdamamAPIFieldValidationError("sys_tag", value)

    @staticmethod
    def _validate_accept_language(value: str) -> None:
        pass


class EdamamQueryBuilder(object):
    def __init__(
        self,
        api_key: str,
        app_id: str,
        edamam_base_url: str,
        included_fields: tuple,
        custom_validator_mapping: dict | None,
        custom_validator_class: object | None,
        db_type: str = "public",
        random: bool = False,
        enable_beta: bool = False,
        enable_account_user_tracking: bool = False,
    ):
        self._prepped_request = PreparedRequest()
        self.enable_beta = enable_beta
        self.enable_account_user_tracking = enable_account_user_tracking
        self.api_key = api_key
        self.edamam_base_url = edamam_base_url
        self.app_id = app_id
        self.db_type = db_type
        self.included_fields = included_fields
        self._current_url = ""
        self.random = random
        self.custom_validator_mapping = custom_validator_mapping
        self.custom_validator_class = custom_validator_class
        self._gen_initial_url()

    def __str__(self):
        return f"Current state of the generated URL: {self._current_url}"

    def _gen_initial_url(self) -> None:
        """

        :return:
        """
        self._prepped_request.prepare_url(
            self.edamam_base_url,
            {
                "app_id": self.app_id,
                "app_key": self.api_key,
                "random": self.random,
                "type": self.db_type,
            },
        )
        self._current_url = self._prepped_request.url

        if not self.included_fields:
            return
        for key in self.included_fields:
            self._prepped_request.prepare_url(self._current_url, {"field": key})
            self._current_url = self._prepped_request.url

    def get_current_url(self) -> str:
        """
        Gets the current built up url, but before runs a validation to the edamam api spec.

        :return:
        """
        self._validate_current_url()
        return self._current_url

    def _validate_current_url(self) -> None:
        """
        Validates the current url.

        :return:
        """
        errs = [
            "app_id" not in self._current_url,
            "app_key" not in self._current_url,
            "type" not in self._current_url,
            ("q" not in self._current_url)
            and all(
                [
                    key not in self._current_url
                    for key in API_FIELD_VALIDATOR_MAPPING.keys()
                ]
            ),
        ]

        if any(errs):
            raise EdamamURLValidationError(
                f"Edamam API URL is invalid. Given URL: {self._current_url}"
            )

    def append_to_query(self, key: str, value: str):
        """
        Based on the key validation for the value will run and throw an exception if the validation fails.

        :param key:
        :param value:
        :return:
        """
        validate_function = API_FIELD_VALIDATOR_MAPPING.get(key)
        if not hasattr(EdamamFieldValidator, validate_function):
            raise EdamamAPIFieldKeyError(key)
        method = getattr(EdamamFieldValidator, validate_function)
        method(value)

        if (
            self.custom_validator_class is not None
            and self.custom_validator_mapping is not None
        ):
            validate_function = self.custom_validator_mapping.get(key)
            if not hasattr(self.custom_validator_class, validate_function):
                raise EdamamAPIFieldKeyError(key)
            method = getattr(self.custom_validator_class, validate_function)
            method(value)

        self._prepped_request.prepare_url(self._current_url, {key: value})
        self._current_url = self._prepped_request.url


class EdamamAPIHandler(object):
    def __init__(self, settings: ApiSettings):
        self.query_builder = EdamamQueryBuilder(**settings.model_dump())
        self.previous_return_data: None | EdamamResponse = None
        self.current_return_data: None | EdamamResponse = None

    def extend_query(self, key, value):
        """
        Main method to use.
        Provide the field which you want to set as the key and the value you want to set it as the value.
        This method will throw an exception if either the base field validator or the custom one you supplied
        raise an exception.

        Field to check has no validtor function on the validator class -> EdamamAPIFieldKeyError
        Field validation failed -> EdamamAPIFieldValidationError

        :param key:
        :param value:
        :return:
        :raises: EdamamAPIFieldKeyError | EdamamAPIFieldValidationError
        """
        self.query_builder.append_to_query(key, value)

    def _get_full_url(self):
        """
        Only call this once you are confident you have every parameter set.

        :return:
        """
        return self.query_builder.get_current_url()

    async def a_request_recipes(self):
        if self.current_return_data:
            ret = request(
                "get",
                self.current_return_data.links.next.href,
            )
        else:
            ret = request("get", self._get_full_url())
        if ret.status_code != 200:
            raise EdamamAPIException(
                ret=ret.json(), status_code=ret.status_code, additional_message=ret.text
            )
        return EdamamResponse(**ret.json())

    def request_recipes(self):
        if self.current_return_data:
            ret = request(
                "get",
                self.current_return_data.links.next.href,
            )
        else:
            ret = request("get", self._get_full_url())

        if ret.status_code != 200:
            raise EdamamAPIException(
                ret=ret.json(), status_code=ret.status_code, additional_message=ret.text
            )
        return EdamamResponse(**ret.json())

    def __iter__(self):
        return self

    def __next__(self):
        self.previous_return_data = self.current_return_data
        self.current_return_data = self.request_recipes()

        if self.current_return_data.links.next is None:
            raise StopIteration

        return self.current_return_data

    def __aiter__(self):
        return self

    async def __anext__(self):
        self.previous_return_data = self.current_return_data
        self.current_return_data = await self.a_request_recipes()

        if self.current_return_data.links.next is None:
            raise StopAsyncIteration

        return self.current_return_data
