#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
from Movie.helper import agents, referers

class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        referer = random.choice(referers)
        agent = random.choice(agents)
        #request.headers['Referer'] = referer
        request.headers["User-Agent"] = agent
