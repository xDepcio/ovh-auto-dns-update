import ovh


class OVHApiController:

    def __init__(self, client: ovh.Client, domain: str):
        self.client = client
        self.domain = domain

    def delete_A_record(self, record_id: str):
        return self.client.delete(f"/domain/zone/{self.domain}/record/{record_id}")

    def get_A_record_id(self, subdomain: str):
        result = self.client.get(
            f"/domain/zone/{self.domain}/record", fieldType="A", subDomain=subdomain
        )
        if type(result) != list:
            raise Exception("Error while fetching A record ID")

        if len(result) == 0:
            return None

        return result[0]

    def add_A_record(self, subdomain: str, target: str):
        return self.client.post(
            f"/domain/zone/{self.domain}/record/",
            target=target,
            subDomain=subdomain,
            fieldType="A",
        )

    def refresh_dns_zone(self):
        return self.client.post(f"/domain/zone/{self.domain}/refresh")
