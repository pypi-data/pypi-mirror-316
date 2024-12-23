# Suits ⚖️

Your intelligent Python assistant that operates directly on your code objects, powered by Google's Gemini AI.

## Why Suits?

Ever wished you could just tell your code what you want it to do? That's exactly what Suits offers. Unlike traditional chatbots or AI assistants that just provide suggestions, Suits works directly with your Python objects in real-time.

### What Makes Suits Different?
- **Direct Object Manipulation**: Operates on your actual data structures, not just text
- **Real-time Integration**: Results can be immediately used in your code
- **Natural Language Interface**: No need to remember complex APIs or methods
- **Intelligent Understanding**: Grasps context and intent from your instructions

### Perfect For:
- Data scientists cleaning messy datasets
- Developers prototyping ideas quickly
- Anyone who wants to experiment with data transformations
- Quick proof-of-concepts before writing formal code

## Real-World Examples

### Data Cleaning & Analysis
```python
# Messy data with inconsistent formats
data = [
    {"date": "2023-01-01", "temp": "25C"},
    {"date": "Jan 2, 2023", "temp": "77F"},
    {"date": "03/01/2023", "temp": "298K"}
]

donna = Donna(data)
donna.briefing(api_key="your-api-key")

# One line to standardize everything
clean_data = donna.i_need_you_to("standardize all dates to ISO format and temperatures to Celsius")
# Result: [
#   {"date": "2023-01-01", "temp": 25.0},
#   {"date": "2023-01-02", "temp": 25.0},
#   {"date": "2023-01-03", "temp": 25.0}
# ]
```

### Pattern Recognition
```python
# Sequence with non-obvious pattern
numbers = [102, 105, 110, 115, 122, 131, 142]

donna = Donna(numbers)
donna.briefing(api_key="your-api-key")

# Understanding and extending patterns
next_values = donna.i_need_you_to("find the pattern and predict the next 3 values")
# Result: [155, 170, 187]
```

### System Analysis with Reasoning
```python
system_data = {
    'server_status': 'running',
    'cpu_usage': 95,
    'memory': '2%',
    'disk_space': '90%',
    'response_time': '3000ms'
}

donna = Donna(system_data)
donna.briefing(api_key="your-api-key")

analysis = donna.i_need_you_to("analyze system health", reasoning=True)
# Result:
# <thinking>
# Examining key metrics:
# 1. CPU usage is extremely high at 95%
# 2. Disk space is concerning at 90%
# 3. Memory usage is surprisingly low at 2%
# This pattern suggests...
# </thinking>
# <output>
# Critical issues detected: High CPU usage (95%) and high disk space usage (90%)
# </output>
```

## Installation
```bash
pip install suits
```

## Features

### Basic Usage
Ask Donna to perform any task on your data in plain English:
```python
data = [1, "2", None, "4", 5.0]
donna = Donna(data)
donna.briefing(api_key="your-api-key")

# Clean and standardize data
result = donna.i_need_you_to("clean this list and make all elements integers")
```

### Structured Output
Need results in a specific format? Define a schema class and Donna will deliver:
```python
class AnalysisSchema:
    summary: str
    count: int
    
result = donna.i_need_you_to("analyze this data", output_config=AnalysisSchema)
# Returns: {"summary": "...", "count": 42}
```

### Reasoning Mode
Want to see Donna's thought process? Enable reasoning mode:
```python
result = donna.i_need_you_to("solve this complex problem", reasoning=True)
# Returns:
# <thinking>First, let's examine the structure...</thinking>
# <output>Final solution here</output>
# <reflection>Actually, we should consider...</reflection>
```

### Temperature Control
Control the creativity vs precision of responses:
```python
# More precise responses
donna.briefing(api_key="key", temperature=0.1)

# More creative responses
donna.briefing(api_key="key", temperature=0.8)
```

## Notes
- `output_config` and `reasoning` modes cannot be used together
- Default temperature is 0.2 for optimal balance
- Requires a Google API key with Gemini access