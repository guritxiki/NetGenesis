import ipaddress

class FullDomain:
    def __init__(self, domain_name, tld, ip_address=None):
        if not self.is_valid_domain_name(domain_name):
            raise ValueError("Invalid domain name")
        if not self.is_valid_tld(tld):
            raise ValueError("Invalid TLD")
        if ip_address and not self.is_valid_ip_address(ip_address):
            raise ValueError("Invalid IP address")
        
        self.domain_name = domain_name
        self.tld = tld
        self.ip_address = ip_address

    def is_valid_domain_name(self, domain_name):
        """Validate the domain name."""
        return isinstance(domain_name, str) and 1 <= len(domain_name) <= 64

    def is_valid_tld(self, tld):
        """Validate the top-level domain (TLD)."""
        return isinstance(tld, str) and 1 <= len(tld) <= 4

    def is_valid_ip_address(self, ip_address):
        """Validate the IP address."""
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            return False

    def get_domain_name(self):
        """Return the domain name part."""
        return self.domain_name

    def get_tld(self):
        """Return the top-level domain (TLD) part."""
        return self.tld

    def get_ip_address(self):
        """Return the IP address."""
        return self.ip_address

    def get_full_domain(self):
        """Return the full domain string."""
        if self.ip_address:
            return f"{self.domain_name}.{self.tld}:{self.ip_address}"
        return f"{self.domain_name}.{self.tld}"

    def serialize(self):
        """Serialize the domain into bytes."""
        serialized = f"{self.domain_name}.{self.tld}"
        if self.ip_address:
            serialized += f":{self.ip_address}"
        return serialized.encode('utf-8')

    @staticmethod
    def parse(serialized):
        """Parse bytes into a FullDomain object."""
        try:
            serialized_str = serialized.decode('utf-8')
            if ':' in serialized_str:
                domain_part, ip_address = serialized_str.split(':', 1)
                domain_name, tld = domain_part.split('.', 1)
                return FullDomain(domain_name, tld, ip_address)
            domain_name, tld = serialized_str.split('.', 1)
            return FullDomain(domain_name, tld)
        except (ValueError, IndexError) as e:
            raise ValueError("Invalid serialized format") from e

    def is_equal_up_to_ip(self, other_domain):
        """Check if two domains are the same up to the IP address."""
        return (self.domain_name == other_domain.domain_name and
                self.tld == other_domain.tld)

    def change_ip(self, new_ip_address):
        """Change the IP address of the domain."""
        if not self.is_valid_ip_address(new_ip_address):
            raise ValueError("Invalid IP address")
        self.ip_address = new_ip_address
