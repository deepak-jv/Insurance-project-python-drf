from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


swagger_info = openapi.Info(
    title='Your API Title',
    default_version='v1',
    description='Your API Description',
    terms_of_service='https://example.com/terms/',
    contact=openapi.Contact(email='contact@example.com'),
    license=openapi.License(name='MIT License'),
)


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)

        # Modify the schema JSON as desired
        schema['info']['title'] = 'Custom API Title'
        schema['info']['description'] = 'Custom API Description'

        return schema

