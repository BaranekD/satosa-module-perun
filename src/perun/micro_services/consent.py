import logging
import json
import requests
from jwkest.jws import JWS
from satosa.micro_services.base import ResponseMicroService
from satosa.response import Redirect
from satosa.internal import InternalData

logger = logging.getLogger(__name__)

STATE_KEY = "CONSENT"


class UnexpectedResponseError(Exception):
    pass


class Consent(ResponseMicroService):

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = "/handle_consent"
        self.name = "consent"

    def process(self, context, data):
        context.state[STATE_KEY] = context.state.get(STATE_KEY, {})
        context.state[STATE_KEY]["data"] = data.to_dict()

        # context.path: Saml2SP/acs/post

        request = "https://ip-78-128-251-177.flt.cloud.muni.cz/flask/abc"
        # res = requests.head(request, allow_redirect=True)
        return Redirect(request)
        # logger.debug(res.__str__)
        # return super().process(context, data)

        # try:
        #     consent_attributes = self._verify_consent()
        # except requests.exceptions.ConnectionError as e:
        #     logger.debug("Consent service is not reachable, no consent is given.")
        #     data.attributes = {}
        #     return super().process(context, data)

        # if consent_attributes is not None:
        #     logger.debug("Previous consent was given")
        #     data.attributes = self._filter_attributes(data.attributes, consent_attributes)
        #     return super().process(context, data)

        # logger.debug("Consent before approve")
        # return self._approve_new_consent(context, data)

    # def _verify_consent(self):
    #     logger.debug('The beginning of verify_consent')
    #     #request = "{}".format(self.base_url + '/abc')
    #     request = "{}".format('https://www.satosa.proxy.cz/')
    #     res = requests.get(request)
    #     logger.debug('After request.get')
    #
    #     if res.status_code == 200:
    #         return json.loads(res.text)
    #
    #     logger.debug('returning None')
    #     return None

    # def _filter_attributes(self, attributes, filter):
    #     return {k: v for k, v in attributes.items() if k in filter}

    def _approve_new_consent(self, context, data):
        logger.debug("The beginning of _approve_new_consent")
        consent_args = {
            "attr": data.attributes,
            "id": 12345,
            "redirect_endpoint": "%s/consent%s" % (self.base_url, "/handle_consent"),
            "requester_name": data.requester_name,
        }
        try:
            logger.debug("Before _consent_registration")
            ticket = self._consent_registration(consent_args)
        except ConnectionError as e:
            data.attributes = {}
            return super().process(context, data)

        logger.debug("Before consent redirect")
        consent_redirect = "%s/%s" % ('https://www.google.com', ticket)
        return consent_redirect

    def _consent_registration(self, consent_args):
        # jws = JWS(json.dumps(consent_args))
        # request = "{}/creq/{}".format('https://satosa.proxy.cz/flask/abc', jws)
        request = "https://satosa.proxy.cz/flask/abc"
        logger.debug("Before request")
        res = requests.get(request)

        if res.status_code != 200:
            raise UnexpectedResponseError("Consent service error: %s %s", res.status_code, res.text)

        logger.debug("Before _consent_registration return")
        return res.text

    def _handle_consent_response(self, context):
        consent_state = context.state[STATE_KEY]
        #saved_resp = consent_state["data"]
        #data = InternalData.from_dict(saved_resp)

        #context.state.pop(STATE_KEY, None)
        #return super().process(context, data)

    def register_endpoints(self):
        """
        Register consent module endpoints
        :rtype: list[(srt, (satosa.context.Context) -> Any)]
        :return: A list of endpoints bound to a function
        """
        return [("^consent%s$" % self.endpoint, self._handle_consent_response)]





    """
    data:
    
    {'auth_info': 
        {'auth_class_ref': 'urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport',
         'timestamp': '2020-06-03T11:11:43Z',
         'issuer': 'https://login.cesnet.cz/github-idp/'
        },
     'requester': 'https://aai-playground.ics.muni.cz/simplesaml/module.php/saml/sp/metadata.php/default-sp',
     'requester_name': [{'text': None, 'lang': 'en'}],
     'subject_id': '41050333@github.extidp.cesnet.cz',
     'subject_type': 'urn:oasis:names:tc:SAML:2.0:nameid-format:transient',
     'attributes': 
        {'organization': ['GitHub'],
         'displayname': ['Dominik Baránek'],
         'edupersonuniqueid': ['41050333@github.extidp.cesnet.cz'],
         'givenname': ['Dominik'],
         'name': ['Dominik Baránek'],
         'surname': ['Baránek'],
         'edupersonprincipalname': ['41050333@github.extidp.cesnet.cz'],
         'edupersonscopedaffiliation': ['affiliate@github.extidp.cesnet.cz']
        }
    }
    """
