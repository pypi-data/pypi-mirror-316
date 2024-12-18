# from monitor.performance import get_website_performance
# from monitor.seo import get_seo_details
# from monitor.ui import get_ui_details
# from monitor.security import get_ssl_certificate, get_http_headers
# from report.pdf_report import generate_pdf_report
# # from report.xlsx_report import generate_xlsx_report
#
#
# def monitor_website(url):
#     performance = get_website_performance(url)
#     seo = get_seo_details(url)
#     ui = get_ui_details(url)
#     security = {
#         "ssl_certificate_status": get_ssl_certificate(url),
#         "http_headers": get_http_headers(url)
#     }
#
#     data = {
#         "url": url,
#         "performance": performance,
#         "seo": seo,
#         "ui": ui,
#         "security": security
#     }
#
#     print("data :::",data)
#
#     # Generate PDF and XLSX reports
#     generate_pdf_report(data, "website_monitoring_report.pdf")
#     # generate_xlsx_report(data, "website_monitoring_report.xlsx")
#
#     return data  # Return collected data for further use or debugging
#
#
# # if __name__ == "__main__":
# #     website_url = "https://cybrosys.com"
# #     monitor_website(website_url)
