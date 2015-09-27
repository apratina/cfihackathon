#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import urllib2
from xml.etree.ElementTree import XML

ERROR_MSG="There was some problem with your request. Please try again."
TXTWEB_APPKEY='d695de91-6678-466a-9eac-c224d2dad20e'
TXTWEB_PUBKEY='06D2B9B7-0A5F-48F1-9C61-664C5B0427AC'
class MainHandler(webapp2.RequestHandler):

    patient_location=''
    patient_name='' #patient's name
    patient_age='' #patient's age
    medical_condition='' #disease
    patient_mobile=''

    def getTxtWebHTMLResponse(self):
        return '<html>'+\
               '<head><meta name=\"txtweb-appkey\" content=\"'+TXTWEB_APPKEY+'\"></head>'+\
               '<body>Hi '+self.patient_name+', we will forward your details '+self.patient_mobile+' to the nearest medical facility. Please contact 1800 180 1104</body>'+\
                '</html>'

    def validateRequest(self):
        if self.request.get('txtweb-message') is None:
            self.response.write(self.getTxtWebHTMLResponse(ERROR_MSG))
            self.response.abort(500)

    def getMobileNumberFromHash(self):
        xml_response=urllib2.urlopen('http://api.txtweb.com/v1/mobile/get?txtweb-mobile='+self.request.get('txtweb-mobile')
                               +'&txtweb-appkey='+TXTWEB_APPKEY
                               +'&txtweb-pubkey='+TXTWEB_PUBKEY).read()
        return XML(xml_response).find('mobile-number').text

    def extractRequestParams(self):
        full_patient_details=self.request.get('txtweb-message')
        self.patient_location=full_patient_details.split(' ')[0]
        self.patient_name=full_patient_details.split(' ')[1]
        self.medical_condition=full_patient_details.split(' ')[2]
        self.patient_age=full_patient_details.split(' ')[3]
        self.patient_mobile=self.getMobileNumberFromHash()


    def get(self):
        self.extractRequestParams()
        self.response.write(self.getTxtWebHTMLResponse())

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
