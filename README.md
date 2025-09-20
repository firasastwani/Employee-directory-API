# Agent Learning API

A simple FastAPI application designed to simulate real-world API scenarios for agent development and testing.

## Features

### 🎯 Multiple API Endpoints

- **Employees**: `/employees` - Get employee data with filtering and pagination
- **Departments**: `/departments` - Department information and budgets
- **Projects**: `/projects` - Project management data
- **Search**: `/search` - Universal search across all data types
- **Health**: `/health` - Health check for monitoring
- **Stats**: `/stats` - System statistics

### 🚨 Error Scenarios

- **404 Errors**: Simulated "not found" responses
- **500 Errors**: Database timeouts and internal server errors
- **503 Errors**: Service temporarily unavailable
- **504 Errors**: Gateway timeouts

### ⚡ Performance Testing

- **Random Delays**: 0.1-2.0 second latency simulation
- **Variable Error Rates**: Different error rates per endpoint
- **Async Operations**: Non-blocking I/O simulation

### 📊 Partial Data Scenarios

- **Missing Phone Numbers**: Some employees have `null` phone fields
- **Missing Managers**: Some employees have `null` manager_id
- **Incomplete Information**: Realistic data gaps for testing

### 🔍 Search Functionality

- **Universal Search**: Search across employees, departments, and projects
- **Type Filtering**: Search specific data types
- **Fuzzy Matching**: Case-insensitive partial matches

## Quick Start

### Installation

1. **Create and activate virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   python main.py
   ```

4. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## API Usage Examples

### Basic Employee Queries

```bash
# Get all employees
curl http://localhost:8000/employees

# Get specific employee
curl http://localhost:8000/employees/1

# Filter by department
curl "http://localhost:8000/employees?department=Engineering"

# Pagination
curl "http://localhost:8000/employees?limit=5&offset=0"

# Get employee salary
curl http://localhost:8000/employees/1/salary
```

### Search Functionality

```bash
# Universal search
curl "http://localhost:8000/search?q=engineering"

# Search specific type
curl "http://localhost:8000/search?q=alice&type=employees"

# Search departments
curl "http://localhost:8000/search?q=marketing&type=departments"
```

### Department and Project Queries

```bash
# Get all departments
curl http://localhost:8000/departments

# Get specific department
curl http://localhost:8000/departments/Engineering

# Get projects by status
curl "http://localhost:8000/projects?status=active"

# Get projects by department
curl "http://localhost:8000/projects?department=Engineering"
```

### System Endpoints

```bash
# Health check
curl http://localhost:8000/health

# System statistics
curl http://localhost:8000/stats
```

## Error Handling

The API simulates various real-world error scenarios:

- **404 Not Found**: Invalid IDs or non-existent resources
- **500 Internal Server Error**: Database timeouts and connection issues
- **503 Service Unavailable**: Temporary service disruptions
- **504 Gateway Timeout**: Request timeout scenarios

## Data Structure

### Employee Data

```json
{
  "id": 1,
  "name": "Alice Johnson",
  "department": "Engineering",
  "phone": "+1-555-0101", // Can be null
  "manager_id": 5, // Can be null for managers
  "hire_date": "2022-01-15",
  "salary": 95000 // Available via /salary endpoint
}
```

### Department Data

```json
{
  "name": "Engineering",
  "head": "Eva Martinez",
  "budget": 5000000,
  "location": "Building A, Floor 3"
}
```

### Project Data

```json
{
  "id": 1,
  "name": "Mobile App Redesign",
  "department": "Engineering",
  "status": "active",
  "budget": 150000,
  "start_date": "2023-06-01"
}
```

## Agent Development Use Cases

This API is perfect for testing:

1. **Error Recovery**: How agents handle various HTTP error codes
2. **Data Parsing**: Handling partial/missing data fields
3. **Rate Limiting**: Dealing with variable response times
4. **Search Logic**: Implementing fuzzy search across multiple data types
5. **Pagination**: Handling large datasets with offset/limit
6. **Monitoring**: Health checks and system statistics
7. **Retry Logic**: Dealing with transient failures
8. **Data Aggregation**: Combining data from multiple endpoints

## Configuration

### Error Rates by Endpoint

- `/employees`: 5-10% error rate
- `/departments`: 3-5% error rate
- `/projects`: 7-8% error rate
- `/search`: 6% error rate
- `/health`: 2% failure rate

### Performance Simulation

- **Latency Range**: 0.1-2.0 seconds
- **Async Operations**: All endpoints use async/await
- **Random Delays**: Simulates real-world network conditions

## Sample Data

The API includes realistic sample data:

- **10 employees** across 4 departments
- **4 departments** with budget and location info
- **5 projects** in various statuses
- **Partial data** with missing phone numbers and manager relationships

## Development

### Adding New Endpoints

1. Define Pydantic models for request/response validation
2. Add sample data to the appropriate data dictionary
3. Implement the endpoint with error simulation
4. Update documentation

### Customizing Error Rates

Modify the `simulate_error()` function calls in each endpoint to adjust error frequencies for your testing needs.

### Adding New Data Types

1. Create new data dictionary
2. Add corresponding Pydantic models
3. Implement CRUD endpoints
4. Update search functionality

## License

This project is designed for educational purposes in agent development and API testing.
# Employee-directory-API
