MESSAGES = {
    # Login
    "LOGIN_SUCCESS": "Login successful.",
    "LOGIN_FAILED": "Login failed.",
    "USER_NOT_FOUND": "User not found.",
    "USER_BLOCKED": "You have been blocked.",
    "INVALID_CREDENTIALS": "Invalid email or password.",
    "VALIDATION_ERROR": "Validation failed. Please check your input.",
    "TOKEN_GENERATION_FAILED": "Failed to generate authentication token.",
    "NOTIFICATION_CREATION_FAILED": "Failed to create login notification.",
    "LOG_ACTIVITY_FAILED": "Failed to log user activity.",
    "ROLE_DATA_RETRIEVAL_FAILED": "Failed to retrieve user role data.",
    "DATABASE_ERROR": "Database error occurred during login.",
    "UNEXPECTED_ERROR": "An unexpected error occurred during login.",


    # Bidding
    # General Messages
    "BIDDING_SUCCESS": "Bidding created successfully.",
    "BIDDING_FETCH_SUCCESS": "Bidding fetched successfully.",
    "BIDDINGS_FETCH_SUCCESS": "Biddings fetched successfully.",
    "BIDDING_UPDATE_SUCCESS": "Bidding updated successfully.",
    "BIDDING_APPROVAL_SUCCESS": "Bidding approved successfully.",
    "BIDDING_DELETE_SUCCESS": "Bidding deleted successfully.",

    # Error Messages
    "INVALID_BID_DATE": "Invalid bidDate format. Use YYYY-MM-DD.",
    "INVALID_DATA": "Invalid data provided.",
    "USER_NOT_FOUND": "User not found or not active.",
    "BIDDING_NOT_FOUND": "Bidding not found.",
    "BIDDING_ERROR":"An error occurred while creating the bidding.",
    "BIDDING_ALREADY_APPROVED": "Bidding already approved.",
    "UNAUTHORIZED_BIDDING_APPROVAL": "You are not authorized to approve this bidding.",
    "TECH_LEAD_NOT_FOUND": "Tech Lead not found.",
    "TEAM_NOT_FOUND": "Specified team not found.",
    "INVALID_DEVELOPER_IDS": "Some developer IDs are invalid: {missing_devs}.",
    "PROJECT_CREATION_FAILED": "Failed to create project for the bidding.",
    "BIDDING_CREATION_FAILED": "Failed to create bidding.",
    "BIDDING_UPDATE_FAILED": "Failed to update bidding.",
    "BIDDING_APPROVAL_FAILED": "An error occurred while approving the bidding.",
    "FILE_UPLOAD_FAILED": "File upload failed.",
    "DATABASE_ERROR": "Database error occurred while processing the bidding request.",
    "UNEXPECTED_ERROR": "An unexpected error occurred while processing the bidding request.",
    "INTERNAL_ERROR":"An internal server error while approving the bidding.",


    # Assignment API Messages
    "INVALID_DATE_FORMAT":"Invalid due_date format. Expected YYYY-MM-DD.",
    "ERROR_OCCURED":"An error occurred",
    "PROJECT_NOT_FOUND": "Project not found.",
    "ASSIGNMENT_FETCH_ERROR": "An error occurred while fetching assignments.",
    "ASSIGNMENT_LIST_FETCH_SUCCESS": "Assignments fetched successfully.",
    "ASSIGNMENTS_FETCH_SUCCESS" : "Assignments fetched successfully.",
    "NO_ASSIGNMENTS_FOUND": "No assignments available for this project.",
    "ASSIGNMENT_NOT_FOUND": "Assignment not found.",
    "INVALID_ASSIGNMENT_DATA": "Invalid assignment data.",
    "ASSIGNMENT_UPDATE_SUCCESS": "Assignment updated successfully.",
    "INVALID_DEVELOPERID":"Invalid developerId",
    "INVALID_TESTERID":"Invalid testerId",
    "ASSIGNMENT_UPDATE_FAILED": "Failed to update assignment.",
    "ASSIGNMENT_DELETE_SUCCESS": "Assignment deleted successfully.",
    "ASSIGNMENT_DELETE_FAILED": "Failed to delete assignment.",
    "INVALID_DEVELOPER_ID": "Invalid developer ID.",
    "INVALID_TESTER_ID": "Invalid tester ID.",
    "INVALID_PROJECT_ID":"Invalid projectID project not found",
    "INTERNAL_SERVER_ERROR":"Internal server error",
    "DEVELOPER_NOT_AUTHORIZED": "You are not authorized to update this assignment.",
    "TESTER_NOT_AUTHORIZED": "You are not authorized to update this assignment.",
    "DEVELOPER_MUST_UPDATE_FIRST": "Developer must update the assignment before the tester can modify it.",
    "INTERNAL_SERVER_ERROR": "Internal server error: {error_message}",
    "ASSIGNMENT_ID_REQUIRED": "Assignment ID is required.",
    "INVALID_ASSIGNMENT_ID": "Assignment ID must be a valid integer.",
    "ASSIGNMENT_REGISTERED_SUCCES":"Registration successfully",
    "ASSIGNMENT_CREATION_SUCCESS": "Assignment created successfully.",
    "ASSIGNMENT_CREATION_FAILED": "Failed to create assignment.",
    "INVALID_ASSIGNMENT_DATA": "Invalid assignment data.",
    "INVALID_DATE_FORMAT": "Invalid date format. Use YYYY-MM-DD.",
    "UNEXPECTED_ERROR":"An unexpected error occurred",
    "UPDATE_FAILED":"Update failed",
    "UNAUTHORIZED_ASSIGNMENT_UPDATE": "Access denied. You are not authorized to update this assignment.",
    "ASSINGMNET_UPDATE_DEVELOPER_ID": "Assignment updated successfully by Developer!",
    "UNAUTHORIZED_TESTER_UPDATE": "Access denied. You are not authorized to update this assignment.",
    "PENDING_ASSIGNMENT_UPDATE": "Developer has not updated the assignment status yet. You cannot update it.",
    "ASSIGNMENT_UPDATED_BY_TESTER": "Assignment updated successfully by Tester!",
    "ASSINGMENT_UPDATE_SUCCESS":"Assignment updated successfully",
    "DATABASE_ERROR":"Database error occurred ",
    
   #Upadte
    "INVALID_ASSIGNMENT_ID": "Assignment ID must be a valid integer.",
    "ASSIGNMENT_ID_REQUIRED": "Invalid assignment Id Assignment ID is required.",
    "ASSIGNMENT_NOT_FOUND": "Assignment not found.",
    "INVALID_DEVELOPER_ID": "Invalid developer ID.",
    "DEVELOPER_NOT_AUTHORIZED": "You are not authorized to update this assignment.",
    "INVALID_DATE_FORMAT": "Invalid date format. Use YYYY-MM-DD.",
    "ASSIGNMENT_UPDATE_SUCCESS": "Assignment updated successfully by Developer!",
    "UPDATE_FAILED": "Update failed.",
    "DATABASE_ERROR": "Database error occurred.",
    "UNEXPECTED_ERROR": "An unexpected error occurred.",
    #Update_By_Tester_id
    "INVALID_ASSIGNMENT_ID": "Assignment ID must be a valid integer.",
    "ASSIGNMENT_ID_REQUIRED": "Assignment ID is required.",
    "ASSIGNMENT_NOT_FOUND": "Assignment not found in the list.",
    "INVALID_TESTER_ID": "Invalid tester ID.",
    "TESTER_NOT_AUTHORIZED": "You are not authorized to update this assignment.",
    "PENDING_ASSIGNMENT_UPDATE": "Developer has not updated the assignment status yet. Tester cannot update it.",
    "INVALID_DATE_FORMAT": "Invalid date format. Use YYYY-MM-DD.",
    "ASSIGNMENT_UPDATED_BY_TESTER": "Assignment updated successfully by Tester!",
    "UPDATE_FAILED": "Update failed.",
    "DATABASE_ERROR": "Database error occurred.",
    "UNEXPECTED_ERROR": "An unexpected error occurred.",
    #Delete 
    "INVALID_ASSIGNMENT_ID": "Assignment ID must be a valid integer.",
    "ASSIGNMENT_ID_REQUIRED": "Assignment ID is required.",
    "ASSIGNMENT_NOT_FOUND": "Assignment not found.",
    "ASSIGNMENT_DELETE_SUCCESS": "Assignment deleted successfully.",
    "ASSIGNMENT_DELETE_FAILED": "Failed to delete assignment.",
    "TESTER_NOT_AUTHORIZED": "You are not authorized to delete this     assignment.",
    "DATABASE_ERROR": "Database error occurred while deleting the   assignment.",
    "UNEXPECTED_ERROR": "An unexpected error occurred while deleting    the assignment.",





    
    #FILE UPLOADER
    "NO_FILE_IN_REQUEST": "No file part in the request.",
    "NO_FILE_SELECTED": "No file selected for upload.",
    "INVALID_FILE_TYPE": "Invalid file type. Allowed types: {allowed_types}.",
    "FILE_UPLOAD_FAILED": "File upload failed.",
  
     #LOGS
    "LOG_ACTIVITY_FAILED": "Failed to log activity.",
    "LOG_ACTIVITY_SUCCESS": "Activity logged successfully.",
    "USER_ID_NOT_FOUND": "User ID not found in the request.",
    "LOGS_FETCH_SUCCESS": "Fetched successfully paginated logs for master_admin",
    "LOGS_FETCH_FAILED": "Failed to fetch logs.",
    "UNAUTHORIZED_ACCESS": "Access denied. You do not have the  required permissions.",
    "INVALID_PAGINATION_PARAMS": "Invalid pagination parameters.       Please provide valid page and per_page values.",
    
    #NOTIFICATION
    "NOTIFICATION_CREATION_SUCCESS": "Notification created successfully.",
    "NOTIFICATION_CREATION_FAILED": "Failed to create notification.",
    "NOTIFICATION_FETCH_SUCCESS": "Notifications fetched successfully.",
    "NOTIFICATION_FETCH_FAILED": "Failed to fetch notifications.",
    "NOTIFICATION_NOT_FOUND": "Notification not found.",
    "NOTIFICATION_MARKED_AS_READ": "Notification marked as read successfully.",
    "NOTIFICATION_MARK_FAILED": "Failed to mark notification as read.",
    "ALL_NOTIFICATIONS_MARKED_AS_READ": "All notifications marked as read successfully.",
    "NO_UNREAD_NOTIFICATIONS": "No unread notifications found.",
    "INTERNAL_SERVER_ERROR": "Internal server error occurred.",
    "DATABASE_ERROR": "Database operation failed.",
    "UNAUTHORIZED_ACCESS": "Access denied. You do not have the required permissions.",
    "INVALID_USER_ID": "Invalid or missing user ID in the request.",

    
    #PAYMNETS:----->
    "PROJECT_ID_REQUIRED": "Project ID is required.",
    "PAYMENT_CREATED_SUCCESS":"Payment created successfully",
    "ERROR_CREATING_PAYMNET":"Error creating payment",
    "INVALID_PROJECT_ID": "Project ID must be a valid integer.",
    "PROJECT_NOT_FOUND": "Project not found.",
    "PAYMENT_FETCHED_SUCCESS":"Payment fetched successfully",
    "PAYMENT_NOT_FOUND_CRIETERIA":"No payments found. Please refine your search criteria.",
    "PAYMENT_UPDATED_SUCCESFULL":"Payment updated successfully",
    "PAYMENT_DELETED_SUCCESFULLY":"Payment deleted successfully",
    
    # PROJECTS:--------->
    "PROJECT_FETCH_SUCCESS": "Project fetched successfully.",
    "PROJECT_FETCH_FAILED": "Failed to fetch project.",
    "PROJECT_NOT_FOUND": "Project not found.",
    "PROJECTS_FETCH_SUCCESS": "Projects fetched successfully.",
    "PROJECTS_FETCH_FAILED": "Failed to fetch projects.",
    "NO_PROJECTS_FOUND": "No projects found. Please refine your search criteria.",
    "INVALID_PROJECT_NAME": "Project name cannot be empty.",
    "INVALID_PAGINATION_PARAMS": "Invalid pagination parameters. Please provide valid page and per_page values.",
    "UNAUTHORIZED_ACCESS": "Access denied. You do not have the required permissions.",
    "INTERNAL_SERVER_ERROR": "Internal server error occurred.",
    "DATABASE_ERROR": "Database operation failed.",

    
    # Role
    "ROLE_CREATION_SUCCESS": "Role created successfully.",
    "ROLE_LIST":"Here is the roles list",
    "VALIDATION_FAILED":"Input validation failed",
    "ROLE_CREATION_FAILED": "Failed to create role.",
    "ROLE_ALREADY_EXISTS": "Role '{name}' already exists.",
    "ROLE_FETCH_SUCCESS": "Role fetched successfully.",
    "ROLE_FETCH_FAILED": "Failed to fetch role.",
    "ROLE_NOT_FOUND": "Role not found.",
    "ROLES_LIST_FETCH_SUCCESS": "Here is the roles list.",
    "ROLES_LIST_FETCH_FAILED": "Failed to fetch roles list.",
    "ROLE_UPDATE_SUCCESS": "Role updated successfully.",
    "ROLE_UPDATE_FAILED": "Failed to update role.",
    "INVALID_ROLE_ID": "Invalid role ID format.",
    "INVALID_ROLE_NAME": "Role name cannot be empty.",
    "INVALID_PERMISSION_ID": "Invalid permission ID: {perm_id}.",
    "PERMISSION_LIST_FETCH_SUCCESS": "Permission list found.",
    "PERMISSION_LIST_FETCH_FAILED": "Failed to fetch permissions.",
    "PERMISSION_LIST_NOT_FOUND": "permission list found",
    "UNAUTHORIZED_ACCESS": "Access denied. You do not have the required permissions.",
    "INTERNAL_SERVER_ERROR": "Internal server error occurred.",
    "DATABASE_ERROR": "Database operation failed.",

    
    #TEAMS
    "INVALID_DEVELOPER_IDS":"Invalid Developers ID",
    "INTEGRITY_ERROR":"Integrity error occurred",
    "TEAM_CREATED_SUCCESS":"Team created successfully",
    "TEAM_NOT_FOUND":"Team not found",
    "TEAM_UPDATE_SUCCESS":"Team Updated Succesfully",
    "TEAM_FETCHED_SUCCESS":"All Teams Fetched successfully",
    
    # JWT
    "TOKEN_MISSING": "Token is missing. Please provide a valid token.",
    "SECRET_KEY":"SECRET_KEY must be a string",
    "TOKEN_INVALID": "Invalid token,Token has expired, Please log in again.",
    "TOKEN_EXPIRED": "Token has expired. Please log in again.",
    "TOKEN_CREATION_FAILED": "Failed to generate token.",
    "TOKEN_VERIFICATION_FAILED": "Token verification failed.",
    "TOKEN_ALREADY_EXISTS": "A valid token already exists for   this user.",
    "TOKEN_GENERATED_SUCCESS": "Token generated successfully.",
    "ACCESS_FORBIDDEN": "Access forbidden: This API is only     accessible by {roles}.",
    "USER_NOT_AUTHENTICATED": "User not authenticated. Please log   in.",
    "USER_NOT_FOUND": "User not found.",
    "USER_ROLE_NOT_FOUND": "User role not found.",
    "USER_PERMISSION_NOT_FOUND": "User permissions not found.",
    "PERMISSION_DENIED": "Access forbidden: Missing required    permissions.",

    
    # USER
    "EMPLOYEE_ALREADY_EXITS":"Employee ID already exists",
    "REGISTRATION_SUCCESFULL":"Registration successfully",
    "USER_FETCH_UNSUCCESS":"Failed to fetch users",
    "REGISTRATION_UNSUCCESFULL":"registration unsuccessfully",
    "EMPLOYEE_ALREADY_EXISTS_UNSUCESS_ID":'Register,Registration unsuccessful - Employee ID already exists',
    "REGISTRATION_UNSUCCESFULL_NAME":'Register ,Registration unsuccessful - Name already exists',
    "USER_FIRST_LAST_NAME_EXISTS":"A user with this first and last name already exists.",
    "USER_EMAIL_ALREADY_EXISTS":'Register ,Registration unsuccessful - Email already exists',
    "USER_EMAIL_ALREADY_REGISTERD":"This email is already registered.",
    "USER_MOBILE_ALREADY_EXISTS":'Register, Registration unsuccessful - Mobile number already exists',
    "USER_MOBILE_ALREADY_REGISTERD":"This mobile number is already registered.",
    "FAILED_CREATE_USER":"Failed to create user",
    "USER_REGISTRATION_SUCCESS":'Register ,Registration successful',
    "USER_REGISTERED_SUCCES":"User registered successfully",
    "REGISTRATION_FAILED_DATABASE_ERROR":'Register ,Registration failed - Database error',
    "VALIDATION_ERROR":"Validation Error",
    "DATABASE_ERROR":"Database Error",
    "UNEXPECTED_ERROR":'Register ,Registration failed - Unexpected error',
    "UNEXPECTED_ERROR_OCCURED": "An unexpected error occurred.",
    "NO_DATA_FOUND_SEARCH":"No data found matching the search criteria.",
    "USER_FETCHED_SUCCESS":"Users fetched successfully",
    "USER_NOT_FOUND":'User not found',
    "NO_INPUT_DATA_PROVIDED":'No input data provided',
    "USER_UPDATED_SUCCES":"User updated successfully",
    "USER_UPDATE_UNSUCESS":"Update unsuccessful - Internal server error",
    "UPDATE_FAILED":"Failed to update user",
    "USER_UPDATE_FAILED":"No input data provided",
    "USER_DELETED":'User deleted',
    "MASTER_ADMIN_CANNOT_BE_BLOCKED":'Master admin can not be block',
    "USER_ALREADY_BLOCKED":'User Already Blocked',
    "USER_BLOCKED_SUCCESFULL":"User blocked successfully",
    "UPDATE_UNSUCESS":"Update unsuccessful - User not found",
    "NO_USERS_EXISTS":"No user exists with the given ID",
    "DELETE_UNSUCCESFULL":"Delete unsuccessful - User not found",
    "USER_NOT_ACT_EXIST":"No user exists with the given ID",
    "USER_DELETE_SUCCES":"User deleted successfully",
    "USER_DELETE_ERROR":"Delete unsuccessful - Internal server error",
    "FAILED_DELETE":"Failed to delete user",
    
    "BLOCK_NO_INPUT": "Block unsuccessful - No input data provided.",
    "BLOCK_USER_NOT_FOUND": "Block unsuccessful - No user exists with the given ID.",
    "BLOCK_MASTER_ADMIN_NOT_ALLOWED": "Block unsuccessful - Cannot block master admin.",
    "BLOCK_ALREADY_BLOCKED": "Block unsuccessful - User is already blocked.",
    "BLOCK_SUCCESS": "User blocked successfully.",
    "BLOCK_FAILED": "Block unsuccessful - Internal server error.",
    "FAILED_USER":"Failed to block user"

}   
