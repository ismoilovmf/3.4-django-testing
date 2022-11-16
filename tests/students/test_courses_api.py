import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Student, Course

URL = '/api/v1/courses/'

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, make_m2m=True, *args, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, make_m2m=True, *args, **kwargs)
    return factory

@pytest.fixture
def create_course(client):
    def creater():
        body = {'name': 'Course_1', 'students': []}
        return [body, client.post(URL, body)]
    return creater

@pytest.mark.django_db
def test_retrieve_course(client, course_factory):
    course = course_factory()
    response = client.get(f'{URL}{course.id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course.name

@pytest.mark.django_db
def test_list_course(client, course_factory):
    course_factory(_quantity=10)
    response = client.get(URL)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10

@pytest.mark.django_db
def test_course_filter_id(client, course_factory):
    courses = course_factory(_quantity=10)
    query = Course.objects.filter(id=courses[3].id)
    response = client.get(f'{URL}?id={query[0].id}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[3].name

@pytest.mark.django_db
def test_course_filter_name(client, course_factory):
    courses = course_factory(_quantity=10)
    query = Course.objects.filter(name=courses[7].name)
    response = client.get(f'{URL}?name={query[0].name}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[7].name

@pytest.mark.django_db
def test_create_course(client, create_course):
    body, response = create_course()
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == body['name']

@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory()
    body = {'name': 'Course_2', 'students': []}
    response = client.patch(f'{URL}{course.id}/', body)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == body['name']

@pytest.mark.django_db
def test_destroy_course(client, create_course):
    body, response = create_course()
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == body['name']
    response = client.delete(f'{URL}{response.data["id"]}/')
    assert response.status_code == 204