# Search settings
KEYWORD_FILTER = "Data Analyst"
LOCATION_FILTER = "Austin, TX"

# Other settings
MAX_PAGES_COMPANIES = 500
MAX_PAGES_REVIEWS = 500

import os
import re
from datetime import datetime
from pymongo import MongoClient
import indeed
import glassdoor
import utils

client = MongoClient()
indeed_db = client.indeed
indeed_jobs = indeed_db.jobs
indeed_reviews = indeed_db.reviews
glassdoor_db = client.glassdoor
glassdoor_reviews = glassdoor_db.reviews

# get job listings
jobs = indeed.get_jobs(KEYWORD_FILTER, LOCATION_FILTER, indeed_jobs, MAX_PAGES_COMPANIES)

# get company reviews
indeed.get_all_company_reviews(jobs, indeed_reviews, MAX_PAGES_REVIEWS)

indeed_reviews.find_one()

companies = list(set(utils.get_company_names(indeed_reviews)))
companies[:5]

'''
fix_companies = {'Argus, ISO, Verisk Analytics, Verisk Climate, Veri...': 'Verisk Analytics',
                 'Barclays Investment Bank': 'Barclays', 'Dun & Brandstreet': u'Dun & Bradstreet',
                 'Dun & Broadstreet':u'Dun & Bradstreet', 'World Business Lenders - New York, NY':'World Business Lenders'
                }
utils.fix_all_company_names(indeed_reviews, fix_companies)
'''

# scrape glassdoor
visited_companies, failed_companies = glassdoor.get_all_company_reviews(companies,
                                              glassdoor_reviews, MAX_PAGES_REVIEWS)

# fix_companies = {u'SigmaTek':u'SigmaTek Consulting LLC',
#                 }
# utils.fix_all_company_names(indeed_reviews, fix_companies)
# fixed_failed_companies = fixed_failed_companies = [utils.fix_company_name(company,
# fix_companies, True) for company in failed_companies]
# visited_companies2, failed_companies = glassdoor.get_all_company_reviews(fixed_failed_companies,
#                                               glassdoor_reviews, MAX_PAGES_REVIEWS)

glassdoor_companies = set(utils.get_company_names(glassdoor_reviews))
indeed_companies = set(utils.get_company_names(indeed_reviews))

# Remove the extra companies:
extra_companies = glassdoor_companies - indeed_companies
for company in extra_companies:
    glassdoor_reviews.remove({'company' : company})

print "Missing companies", indeed_companies - glassdoor_companies