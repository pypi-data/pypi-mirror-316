# Minutes Mail - Temporary Email Manager

This is a Python library that provides a convenient way to create and manage temporary email addresses using two different services: `inboxes.com` and `privatix-temp-mail-v1.p.rapidapi.com`.

## Features

- Create temporary email addresses
- Retrieve a list of available domains for email creation
- Read emails received in the temporary inbox and extract activation codes
- Delete temporary email addresses

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies:

```
pip install minutes-mail
```

## Usage

1. Import the `Mail` class :

```python
from minutes_mail import MinutesMail
```

2. Create an instance of the `Mail` class, specifying the `rapid_api_key` and `proxy_url` if needed:

```python
# With rapid_api_key
mail = MinutesMail.create_instance(email_type='rapid_api',rapid_api_key="your_rapid_api_key", proxy_url="http://your_proxy_url")

# Without rapid_api_key
mail = MinutesMail.create_instance(email_type='1secmail',proxy_url="http://your_proxy_url")
```

The `create_instance` method will automatically create an instance of either `RapidMail` or `InboxesMail` based on whether a `rapid_api_key` is provided or not.

3. Use the available methods to manage the temporary email:

```python
# Create a new email
email = MinutesMail.create_mail()

# Get available domains
domains = MinutesMail.get_domains()

# Read emails and get activation code
code = MinutesMail.get_activation_code(max_wait_minutes=3)

# Delete the email ONLY IN INBOXES CURRENT!
MinutesMail.delete_email(email=email)
```

## Code Structure

- `base_class.py`: Contains the base class `BaseClass` that defines the common interface and properties for the two email services.
- `inboxes_mail.py`: Implements the `InboxesMail` class that interacts with the `inboxes.com` API.
- `rapid_mail.py`: Implements the `RapidMail` class that interacts with the `privatix-temp-mail-v1.p.rapidapi.com` API.
- `mail.py`: Provides a factory method `create_instance` to create an instance of either `RapidMail` or `InboxesMail` based on the provided `rapid_api_key`.

## Dependencies

- `loguru`: For logging purposes.
- `httpx`: For making HTTP requests.
- `bs4` (BeautifulSoup): For parsing HTML content (used by `InboxesMail`).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.