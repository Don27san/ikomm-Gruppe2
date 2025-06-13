import dns.resolver
import dns.message
import dns.query
import dns.exception


class DNSResolver:
    """Class to handle DNS resolution and tracing."""
    @staticmethod
    def resolve_domain_name(domain_name):
        """
        Resolve a domain name to an IP address with tracing.

        :param domain_name: The domain name to resolve.
        :return: A tuple containing the official name, aliases, IP addresses, and trace information.
        """
        trace = []
        try:
            resolver = dns.resolver.Resolver()
            resolver.use_edns(0, 0, 1232)
            resolver.nameservers = ['8.8.8.8', '8.8.4.4']  # Using Google's public DNS servers

            response = resolver.resolve(domain_name, 'A')
            trace.append(f"Resolved using Google's public DNS servers: {resolver.nameservers}")

            ip_addresses = [answer.address for answer in response]
            return (domain_name, [], ip_addresses), trace

        except dns.exception.DNSException as e:
            trace.append(f"DNS lookup failed with Google's public DNS servers: {e}")
            # Fallback to manual root server querying
            try:
                # Query the root servers
                root_ns = resolver.resolve('.', 'NS')
                root_ns_ip = resolver.resolve(root_ns[0].target, 'A')[0].address

                query = dns.message.make_query(domain_name, dns.rdatatype.A)
                response = dns.query.udp(query, root_ns_ip)
                trace.append(f"Queried root server ({root_ns[0].target}): {root_ns_ip}")

                while not response.answer:
                    ns_record = response.additional[0]
                    if ns_record:
                        try:
                            ns_ip = ns_record[0].address
                            trace.append(f"Queried NS ({ns_record.name}): {ns_ip}")
                            response = dns.query.udp(query, ns_ip)
                        except Exception as e:
                            trace.append(f"Failed to query NS ({ns_record.name}): {e}")
                            break
                    else:
                        break

                if response.answer:
                    answer = response.answer[0]
                    trace.append(f"Received final answer from {answer.name}")

                    official_name = answer.name.to_text()
                    ip_addresses = [str(item) for item in answer.items]
                    return (official_name, [], ip_addresses), trace
                else:
                    raise Exception("No answer received")
            except Exception as e:
                trace.append(f"DNS lookup failed with UDP: {e}")
                # Retry using TCP
                try:
                    response = dns.query.tcp(query, root_ns_ip)
                    trace.append(f"Retried root server ({root_ns[0].target}) with TCP: {root_ns_ip}")

                    while not response.answer:
                        ns_record = response.additional[0]
                        if ns_record:
                            try:
                                ns_ip = ns_record[0].address
                                trace.append(f"Retried NS ({ns_record.name}) with TCP: {ns_ip}")
                                response = dns.query.tcp(query, ns_ip)
                            except Exception as e:
                                trace.append(f"Failed to query NS ({ns_record.name}) with TCP: {e}")
                                break
                        else:
                            break

                    if response.answer:
                        answer = response.answer[0]
                        trace.append(f"Received final answer from {answer.name} with TCP")

                        official_name = answer.name.to_text()
                        ip_addresses = [str(item) for item in answer.items]
                        return (official_name, [], ip_addresses), trace
                    else:
                        raise Exception("No answer received with TCP")
                except Exception as e:
                    trace.append(f"DNS lookup failed with TCP: {e}")
                    return None, trace

    @staticmethod
    def dns_request(domain_name):
        """
        Perform a DNS lookup for the domain name.

        :param domain_name: The domain name to lookup.
        :return: A formatted string with the DNS resolution result.
        """
        result, trace = DNSResolver.resolve_domain_name(domain_name)
        output = []
        if result:
            official_name, aliases, ip_addresses = result
            output.append(f"Domain: {domain_name}")
            output.append(f"Official Name: {official_name}")
            output.append(f"Aliases: {aliases}")
            output.append(f"IP Addresses: {ip_addresses}")
        else:
            output.append("DNS lookup failed")

        output.append("Trace:")
        output.extend(trace)

        return "\n".join(output)


if __name__ == "__main__":
    # Loop that checks for domain name inputs
    while True:
        domain_name_input = input("Enter a domain name (or 'quit' to exit): ")
        if domain_name_input.lower() == 'quit':
            break
        dns_result = DNSResolver.dns_request(domain_name_input)
        print(dns_result)
