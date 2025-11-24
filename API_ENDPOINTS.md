# ODH Receptionist Panel - API Endpoints

**Base URL**: `https://acd8c061-b630-4347-a427-0ca5e846f3dc-00-3thwfgq0yvwv5.riker.replit.dev`

**⚠️ SECURITY NOTE**: 
- A default admin user is automatically created on first startup for initial access
- The default credentials are displayed in the console logs on first run
- **CRITICAL**: You MUST change the default admin password immediately after first login
- To change credentials: Login → Admin Dashboard → User Management → Update admin user
- Never use default credentials in production environments

---

## 🔐 Authentication Endpoints

### 1. Login Page
- **GET** `/`
- **Description**: Login page (redirects to dashboard if already logged in)
- **Response**: HTML login form

### 2. Login
- **POST** `/login`
- **Description**: User login endpoint
- **Form Data**:
  - `username`: string (required)
  - `password`: string (required)
- **Response**: Redirects to `/admin/dashboard` or `/receptionist/dashboard` based on role

### 3. Logout
- **GET** `/logout`
- **Description**: Logout user and clear session
- **Response**: Redirects to `/`

---

## 👨‍💼 Admin Endpoints

### User Management

#### 4. List All Users
- **GET** `/admin/users?page={page}`
- **Description**: View all system users with pagination
- **Auth**: Admin only
- **Response**: HTML page with user list

#### 5. Create User
- **POST** `/admin/users`
- **Description**: Create a new user
- **Auth**: Admin only
- **Form Data**:
  - `username`: string (required)
  - `password`: string (required)
  - `role`: string (required) - "admin" or "receptionist"

#### 6. Update User
- **PUT** `/admin/users/manage/{user_id}`
- **Description**: Update existing user details
- **Auth**: Admin only
- **Form Data**:
  - `username`: string (optional)
  - `password`: string (optional)
  - `role`: string (optional)

#### 7. Delete User
- **DELETE** `/admin/users/{user_id}`
- **Description**: Delete a user
- **Auth**: Admin only

### Dashboard

#### 8. Admin Dashboard
- **GET** `/admin/dashboard`
- **Description**: Admin dashboard with visitor statistics
- **Auth**: Admin only
- **Response**: HTML dashboard with stats

### Visitor Management

#### 9. View All Visitors
- **GET** `/admin/visitors/all?page={page}&per_page={per_page}`
- **Description**: View all visitors with pagination
- **Auth**: Admin only
- **Response**: HTML page with visitor list

#### 10. View Future Visitors
- **GET** `/admin/visitors/future-visitor`
- **Description**: View scheduled future visitors
- **Auth**: Admin only
- **Response**: HTML page with future visitor list

#### 11. Notify Early Meeting
- **POST** `/admin/notify-early-meeting/{visitor_id}`
- **Description**: Send early meeting notification to visitor
- **Auth**: Admin only

### Employee Management

#### 12. View Employees
- **GET** `/admin/employees`
- **Description**: View all employees
- **Auth**: Admin only
- **Response**: HTML page with employee list

#### 13. Edit Employee Form
- **GET** `/admin/employees/edit`
- **Description**: Show employee edit form
- **Auth**: Admin only

#### 14. Save Employee
- **POST** `/admin/employees/{employee_id}/edit`
- **Description**: Create or update employee
- **Auth**: Admin only
- **Form Data**:
  - `full_name`: string (required)
  - `dob`: string (optional)
  - `gender`: string (optional)
  - `phone`: string (optional)
  - `email`: string (optional)
  - `aadhaar_number`: string (optional)
  - `pan_number`: string (optional)
  - `address`: string (optional)
  - `emergency_name`: string (optional)
  - `emergency_relation`: string (optional)
  - `emergency_phone`: string (optional)

---

## 👔 Receptionist Endpoints

### Dashboard

#### 15. Receptionist Dashboard
- **GET** `/receptionist/dashboard`
- **Description**: Receptionist dashboard with today's visitor stats
- **Auth**: Receptionist only
- **Response**: HTML dashboard with masked visitor data

### Visitor Management

#### 16. View All Visitors
- **GET** `/receptionist/visitors/all?page={page}&per_page={per_page}`
- **Description**: View all visitors (with masked sensitive data)
- **Auth**: Receptionist only
- **Response**: HTML page with visitor list

#### 17. Check-in Visitor
- **POST** `/receptionist/visitors/check-in`
- **Description**: Check-in a new visitor
- **Auth**: Receptionist only
- **Form Data**:
  - `name`: string (required)
  - `company`: string (required)
  - `email`: string (optional)
  - `phone`: string (required)
  - `host`: string (required)
  - `purpose`: string (required)
  - `notes`: string (optional)

#### 18. Edit Visitor Form
- **GET** `/receptionist/visitors/edit/{visitor_id}`
- **Description**: Show visitor edit form
- **Auth**: Receptionist only

#### 19. Update Visitor
- **POST** `/receptionist/visitors/update/{visitor_id}`
- **Description**: Update visitor appointment details
- **Auth**: Receptionist only
- **Form Data**:
  - `appointment_date`: string (required)
  - `appointment_time`: string (required)

#### 20. Checkout Visitor
- **POST** `/checkout/{visitor_id}`
- **Description**: Check out a visitor
- **Auth**: Receptionist only

### Employee Management

#### 21. View Employees
- **GET** `/receptionist/employees`
- **Description**: View employee information
- **Auth**: Receptionist only

---

## 📱 SMS & OTP Endpoints

#### 22. Send SMS/OTP
- **POST** `/sms/send`
- **Description**: Send SMS or OTP to a phone number
- **Request Body** (JSON):
  ```json
  {
    "phone": "string",
    "message": "string"
  }
  ```

#### 23. Verify OTP
- **POST** `/receptionist/visitors/verify-otp`
- **Description**: Verify OTP for visitor
- **Form Data**:
  - `phone`: string (required)
  - `otp`: string (required)
- **Response**: JSON with verification status

---

## 🔌 WebSocket Endpoints

#### 24. Receptionist WebSocket
- **WebSocket** `/ws/receptionist`
- **Description**: Real-time updates for receptionist dashboard
- **Auth**: Receptionist only
- **Usage**: Connect via WebSocket client for live visitor updates

---

## 📊 Database Information

- **Type**: PostgreSQL (Neon-hosted)
- **Connection**: Automatically configured via `DATABASE_URL` environment variable
- **Tables**: Users, Visitors, Employees, OTP

---

## 🛠️ Technical Details

- **Framework**: FastAPI
- **Server**: Uvicorn (running on port 5000)
- **Authentication**: JWT tokens (stored in HTTP-only cookies)
- **Session**: SessionMiddleware for flash messages
- **Templates**: Jinja2
- **Database ORM**: SQLAlchemy (Async)

---

## 📝 Notes

1. All admin endpoints require admin role authentication
2. All receptionist endpoints require receptionist role authentication
3. Visitor data is masked for receptionist users (privacy protection)
4. Default admin user is automatically created on first startup
5. The application uses Indian Standard Time (IST) for timestamps
6. WebSocket connection provides real-time updates for receptionist dashboard
7. OTP functionality is integrated for visitor verification
8. Session-based flash messages for user feedback
