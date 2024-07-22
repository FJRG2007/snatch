class CloudflareException(Exception): pass # Base exception class for cloudscraper for Cloudflare.
class CloudflareLoopProtection(CloudflareException): pass # Exception raised for recursive depth protection.
class CloudflareCode1020(CloudflareException): pass # Exception raised for Cloudflare code 1020 block.
class CloudflareIUAMError(CloudflareException): pass # Error raised for problems extracting IUAM parameters from Cloudflare payload.
class CloudflareChallengeError(CloudflareException): pass # Error raised when a new Cloudflare challenge is detected.
class CloudflareSolveError(CloudflareException): pass # Error raised when there is an issue with solving a Cloudflare challenge.
class CloudflareCaptchaError(CloudflareException): pass # Error raised for problems extracting Captcha parameters from Cloudflare payload.
class CloudflareCaptchaProvider(CloudflareException): pass # Exception raised when no Captcha provider is loaded for Cloudflare.
class CaptchaException(Exception): pass # Base exception class for cloudscraper captcha providers.
class CaptchaServiceUnavailable(CaptchaException): pass # Exception raised for external services that cannot be reached.
class CaptchaAPIError(CaptchaException): pass # Error raised for errors from API responses.
class CaptchaAccountError(CaptchaException): pass # Error raised for captcha provider account problems.
class CaptchaTimeout(CaptchaException): pass # Exception raised when a captcha provider takes too long.
class CaptchaParameter(CaptchaException): pass # Exception raised for bad or missing parameters.
class CaptchaBadJobID(CaptchaException): pass # Exception raised for invalid job IDs.
class CaptchaReportError(CaptchaException): pass # Error raised when a captcha provider is unable to report a bad solve.