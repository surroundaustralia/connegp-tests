import re
import itertools
import warnings

def check_existance_of_alternatives(response, profiles, encodings):
    """
    R.2.3.c
    The server SHOULD represent the alternate profiles information in the HTTP header
    of the response, as per the HTTP Headers functional profile (using a Link header)
    """
    assert 'link' in response.headers

    links = response.headers['link'].split(',')
    supported_profiles = [p.strip() for p in links if 'profile=' in p ]

    '''
    R.2.3.c
    The server SHOULD represent the alternate profiles information in the HTTP header
    of the response, as per the HTTP Headers functional profile (using a Link header)
    '''
    assert all(['rel="alternate"' in p for p in supported_profiles if 'rel="self"' not in p])
    urls = [re.search('<(http.*)>', profile).group(1) for profile in supported_profiles]

    # Check that profile/encoding combinations that are passed to the function
    # i.e: which should exist, are present in the Link Header
    qsa_urls_should_be_present = []
    for p, e in itertools.product(profiles, encodings):
        alternative_found = False
        for full_link in supported_profiles:
            if f'profile="{p}"' in full_link and f'type="{e}"' in full_link:
                qsa_urls_should_be_present.append(re.search("<(http.*)>", full_link).group(1))
                alternative_found = True
                break
        assert alternative_found

    assert len(set(qsa_urls_should_be_present) - set(urls)) == 0

    '''
    R.2.3.d
    [the server] MAY also represent the information in the response body
    in place of the default profile representation of a resource
 
    R.2.3.e
    Where a server does provide alternate profiles information in an HTTP body,
    the server MAY allow clients to negotiate for particular Media Types of the
    response by using the same Media Type negotiation method used for the get resource
    by profile function
    '''
    qsa_urls_in_body   = set(
      re.findall(r"href=\"(\S+_profile=\w+&_mediatype=.*?)\"", str(response.content))
    )

    if qsa_urls_in_body:
      assert len(urls) == len(qsa_urls_in_body)

      if any([url for url in urls if url not in qsa_urls_in_body]):
        warnings.warn("Alternative profile URLs found in default page do not match Link Header!")
      

      # Since assumptions cannot be made on how the data will be presented (table, CSS grid etc.)
      # unable to verify the required information is present, apart from the URLs
      '''
      R.2.4.a - UNTESTED
      Implementations of this specification according to the QSA Functional Profiles
      MUST communicate their alternate representations information as per the
      Alternate Representations Data Model
      
      R.2.4.b - UNTESTED
      They MAY do so using HTTP Link headers, as per the HTTP Headers functional profile,
      or they MAY use other approaches.
      
      R.2.4.c - UNTESTED
      They may do so via HTTP body content, perhaps in HTML or other data models/formats
      '''

