from rest_framework.test import APITestCase

pw = "Strong@12345"


def signup(c, email, name="Test User"):
    c.post("/api/auth/register/", {"name": name, "email": email, "password": pw}, format="json")
    r = c.post("/api/auth/login/", {"email": email, "password": pw}, format="json")
    return r.data["access"]


class AuthTests(APITestCase):
    def test_register_and_login(self):
        r = self.client.post(
            "/api/auth/register/",
            {"name": "Suraj", "email": "s@test.com", "password": pw},
            format="json",
        )
        self.assertEqual(r.status_code, 201)
        self.assertNotIn("password", r.data)

        r = self.client.post("/api/auth/login/", {"email": "s@test.com", "password": pw}, format="json")
        self.assertEqual(r.status_code, 200)
        self.assertIn("access", r.data)

    def test_duplicate_email(self):
        d = {"name": "A", "email": "a@test.com", "password": pw}
        self.client.post("/api/auth/register/", d, format="json")
        r = self.client.post("/api/auth/register/", d, format="json")
        self.assertEqual(r.status_code, 400)

    def test_wrong_password(self):
        signup(self.client, "b@test.com")
        r = self.client.post("/api/auth/login/", {"email": "b@test.com", "password": "nope"}, format="json")
        self.assertEqual(r.status_code, 401)

    def test_protected_without_token(self):
        self.assertEqual(self.client.get("/api/patients/").status_code, 401)


class ApiTests(APITestCase):
    def setUp(self):
        self.t1 = signup(self.client, "one@test.com")
        self.t2 = signup(self.client, "two@test.com")

    def as_user(self, t):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + t)

    def make_patient(self, name="Ravi"):
        return self.client.post(
            "/api/patients/",
            {"name": name, "age": 30, "gender": "M", "phone": "9876543210"},
            format="json",
        )

    def make_doctor(self, email="doc@test.com"):
        return self.client.post(
            "/api/doctors/",
            {"name": "Mehta", "specialization": "Cardiology", "email": email,
             "phone": "9123456780", "experience": 10},
            format="json",
        )

    def test_patient_crud_and_isolation(self):
        self.as_user(self.t1)
        pid = self.make_patient().data["id"]
        self.assertEqual(len(self.client.get("/api/patients/").data), 1)

        r = self.client.put(
            f"/api/patients/{pid}/",
            {"name": "Ravi K", "age": 31, "gender": "M", "phone": "9876543210"},
            format="json",
        )
        self.assertEqual(r.status_code, 200)

        
        self.as_user(self.t2)
        self.assertEqual(self.client.get(f"/api/patients/{pid}/").status_code, 404)
        self.assertEqual(len(self.client.get("/api/patients/").data), 0)

        self.as_user(self.t1)
        self.assertEqual(self.client.delete(f"/api/patients/{pid}/").status_code, 204)

    def test_patient_validation(self):
        self.as_user(self.t1)
        r = self.client.post(
            "/api/patients/",
            {"name": "X", "age": 200, "gender": "M", "phone": "abc"},
            format="json",
        )
        self.assertEqual(r.status_code, 400)

    def test_doctor_permissions(self):
        self.as_user(self.t1)
        did = self.make_doctor().data["id"]

        self.as_user(self.t2)
        self.assertEqual(self.client.get(f"/api/doctors/{did}/").status_code, 200)
        self.assertEqual(self.client.delete(f"/api/doctors/{did}/").status_code, 403)

    def test_mapping_flow(self):
        self.as_user(self.t1)
        pid = self.make_patient().data["id"]
        did = self.make_doctor().data["id"]

        r = self.client.post("/api/mappings/", {"patient": pid, "doctor": did}, format="json")
        self.assertEqual(r.status_code, 201)
        mid = r.data["id"]

        
        r = self.client.post("/api/mappings/", {"patient": pid, "doctor": did}, format="json")
        self.assertEqual(r.status_code, 400)

        self.assertEqual(len(self.client.get("/api/mappings/").data), 1)
        r = self.client.get(f"/api/mappings/{pid}/")
        self.assertEqual(len(r.data["doctors"]), 1)

    
        self.as_user(self.t2)
        r = self.client.post("/api/mappings/", {"patient": pid, "doctor": did}, format="json")
        self.assertEqual(r.status_code, 400)

        self.as_user(self.t1)
        self.assertEqual(self.client.delete(f"/api/mappings/{mid}/").status_code, 204)
