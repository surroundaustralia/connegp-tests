# Content Negotiation by Profile API Tests

This repository contains conformance tests for *Content Negotiation by Profile*
API, outlined in the [requirements](https://w3c.github.io/dx-connegp/connegp/#reqlist)
section of the specification.

These tests use [Tavern](https://taverntesting.github.io/), a plugin for Pytest.

Details about the system under test are passed though environment variables.

* **TEST_HOST**: URL of service under test
* **TEST_SUPPORTED_PROFILES**: List of supported Profile URLs (comma delimited)
* **TEST_SUPPORTED_MEDIATYPES**: List of supported media types (comma delimited)

Before the tests run, values from `TEST_SUPPORTED_PROFILES` and `TEST_SUPPORTED_MEDIATYPES`
are written to `supported_profiles.yaml` and `supported_mediatypes.yaml`.

These files are then included in the Tavern tests, to support _dynamic paramterized_ tests,
and are removed once Pytest has run.

For example running the tests against https://vocabs.gsq.digital:

```
TEST_SUPPORTED_PROFILES=https://www.w3.org/TR/vocab-dcat/,https://schema.org,http://www.w3.org/ns/dx/conneg/altr \
TEST_SUPPORTED_MEDIATYPES=text/html,text/turtle,application/rdf+xml,application/ld+json,application/n-triples \
TEST_HOST=https://vocabs.gsq.digital/ \
pytest
```
