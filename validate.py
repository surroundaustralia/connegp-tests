import re
import itertools
import warnings

def link_in_response_header(response):
    """
    A server implementing content negotiation by profile SHOULD return an HTTP Link header
    containing information about the default and any alternate representations of that
    resource including profiles they conform to.
    """
    assert 'link' in response.headers

    """
    The default representation – the one that will be returned when no specific representation
    is requested – SHOULD be identified by rel="canonical", other representations by rel="alternate"
    """
    links = response.headers['link'].split(',')
    supported_profiles = [p.strip() for p in links if 'profile=' in p ]

    assert len([p for p in supported_profiles if 'rel="canonical"' in p]) == 1, \
      'R.1.1.b: Profile with rel="canonical" was not found'
    
    assert all(['rel="alternate"' in p for p in supported_profiles if 'rel="canonical"' not in p]), \
      'R.1.1.b: All alternative profiles were not identified with rel="alternate"'

def link_indicates_profile_returned(response, requested_profile):
    """
    A server implementing content negotiation by profile MUST respond with an
    HTTP Response header containing a Link header with rel="profile" indicating the profile returned.
    """
    links = response.headers['link'].split(',')

    profile_link_header = [p for p in links if 'rel="profile"' in p ]
    assert len(profile_link_header) == 1
    assert f"<{requested_profile}>" in profile_link_header[0]

def check_existance_of_alternatives(response, profiles, mediatypes):
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

    # Check that profile/mediatype combinations that are passed to the function
    # i.e: which should exist, are present in the Link Header
    qsa_urls_should_be_present = []
    for p, e in itertools.product(profiles, mediatypes):
        alternative_found = False
        for full_link in supported_profiles:
            if f'profile="{p}"' in full_link and f'type="{e}"' in full_link:
                qsa_urls_should_be_present.append(re.search("<(http.*)>", full_link).group(1))
                alternative_found = True
                break

        assert alternative_found, \
         f'Could not find an alternate with profile="{p}" and type="{e}"'

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

