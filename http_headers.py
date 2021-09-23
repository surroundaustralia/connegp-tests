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
