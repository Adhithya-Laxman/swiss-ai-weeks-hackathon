# # reliable_sources.py
# # Dictionary of reliable news sources for disaster information, organized by continent/major countries.
# # URLs point to disaster/humanitarian sections where possible. Expand as needed.

# reliable_news_sources = {
#     "Global": {
#         "ReliefWeb": "https://reliefweb.int/disasters",  # UN OCHA's disaster reports
#         "Start Network": "https://startnetwork.org/",  # Humanitarian alerts and strategies
#         # "Global Humanitarian Overview (OCHA)": "https://www.unocha.org/global-humanitarian-overview",  # UN OCHA summaries
#         # "Santiago Network": "https://unfccc.int/santiago-network/news",  # UNFCCC loss/damage network
#         # "IFRC (International Federation of Red Cross)": "https://www.ifrc.org/emergencies",  # Global disasters, Swiss ties via Swiss Red Cross
#         # "Reuters AlertsNet": "https://www.reuters.com/world/humanitarian/"  # Global humanitarian news
#     },
#     # "Europe": {
#     #     "Euronews Disasters": "https://www.euronews.com/tag/natural-disaster",  # EU-focused
#     #     "Swissinfo (Swiss Ties)": "https://www.swissinfo.ch/eng/tag/natural-disasters/",  # Swiss-specific with international links
#     #     "European Civil Protection": "https://civil-protection-humanitarian-aid.ec.europa.eu/news-stories/news"  # EU alerts, Swiss cooperation via bilateral agreements
#     # },
#     # "Asia": {
#     #     "India - NDTV Disasters": "https://www.ndtv.com/topic/natural-disasters",  # India-focused
#     #     "China Daily Disasters": "https://www.chinadaily.com.cn/cndy/2025-09/disasters",  # China state media (use cautiously; cross-verify)
#     #     "ASEAN Coordinating Centre": "https://ahacentre.org/bulletins/",  # Southeast Asia disasters
#     #     "Glacial Outbreak Management (Himalayas Focus)": "https://www.icimod.org/activity/glacial-lake-outburst-floods/"  # ICIMOD for glacial risks in Asia, ties to Swiss development aid
#     # },
#     # "Africa": {
#     #     "Africa News Disasters": "https://www.africanews.com/tag/natural-disasters/",  # Continent-wide
#     #     "UN OCHA Africa": "https://www.unocha.org/rocca"  # Regional humanitarian overviews
#     # },
#     # "North America": {
#     #     "USA - FEMA News": "https://www.fema.gov/disaster/news",  # US federal disasters
#     #     "Canada - Public Safety": "https://www.publicsafety.gc.ca/cnt/mrgnc-mngmnt/index-en.aspx"  # Canadian emergencies
#     # },
#     # "South America": {
#     #     "Mercopress Disasters": "https://en.mercopress.com/category/disasters",  # Regional focus
#     #     "CEPAL (UN ECLAC)": "https://www.cepal.org/en/topics/natural-disasters"  # Latin America disasters, Swiss ties via UN
#     # },
#     # "Oceania": {
#     #     "Australia ABC Disasters": "https://www.abc.net.au/news/emergency/",  # Australian focus
#     #     "Pacific Islands Forum": "https://www.forumsec.org/news/"  # Pacific disasters
#     # }
# }

# # Example: To use in your scraper
# # from reliable_sources import reliable_news_sources
# # print(reliable_news_sources["Global"]["ReliefWeb"])


# reliable_sources.py
reliable_news_sources = {
    "Global": {
        "ReliefWeb": "https://reliefweb.int/disasters"  # Works well with updated selectors
    },
    "Asia": {
        "ReliefWeb": "https://reliefweb.int/disasters",  # Works well with updated selectors
        # "India - NDTV Disasters": "https://www.ndtv.com/topic/natural-disasters",
        # "China Daily Disasters": "https://www.chinadaily.com.cn/cndy/2025-09/disasters",
        # "ASEAN Coordinating Centre": "https://ahacentre.org/bulletins/",
        # "Glacial Outbreak Management (Himalayas Focus)": "https://www.icimod.org/activity/glacial-lake-outburst-floods/"
    },
    # Add back other categories as needed
}
