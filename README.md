
# **EasyInventory**

## **Executive Summary**
**EasyInventory** is an innovative web application designed to streamline inventory management for organizations of all sizes. Whether you are managing IT equipment, library books, or office supplies, EasyInventory provides a centralized platform for tracking, managing, and auditing inventory efficiently.

With EasyInventory, administrators can add, edit, and remove inventory items, approve or deny user checkout requests, and monitor inventory usage in real time. Users can request and manage equipment checkouts effortlessly, ensuring that inventory is utilized effectively without unnecessary delays.

Why is EasyInventory important? Tracking resources manually using spreadsheets or paper-based systems is prone to errors, inefficiencies, and delays. EasyInventory replaces these outdated methods with an intuitive interface that saves time, reduces costs, and enhances accountability. By providing a powerful backend combined with a user-friendly frontend, EasyInventory ensures that managing inventory becomes seamless and stress-free.

---

## **Installation**

To set up **EasyInventory** locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/EasyInventory.git
   cd EasyInventory
   ```

2. Build the Docker image:
   ```bash
   docker-compose build
   ```

3. Run database migrations:
   ```bash
   docker-compose run web python manage.py migrate
   ```

4. Create a superuser to manage the application:
   ```bash
   docker-compose run web python manage.py createsuperuser
   ```

---

## **Getting Started**

To launch and start using EasyInventory:

1. Start the application:
   ```bash
   docker-compose up
   ```

2. Open your web browser and navigate to:
   - **Application Home**: [http://localhost:8000/administrator/inventory](http://localhost:8000/administrator/inventory)
   - **Admin Dashboard**: [http://localhost:8000/admin](http://localhost:8000/admin)

3. Log in using the superuser credentials you created during the installation process.

4. Explore the features:
   - Administrators can add, edit, and remove equipment, and manage user checkouts.
   - Users can request equipment and view their checkout history.

---

## **License**

The MIT License (MIT)

```plaintext
MIT License

Copyright (c) Mark Magno [2024]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---
