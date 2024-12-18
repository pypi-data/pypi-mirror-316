from flask import Flask, render_template, request, jsonify
import os
from monitor.performance import get_performance_metrics, get_csp_components, get_security_headers, get_internal_links
from monitor.seo import get_seo_details
from monitor.ui import get_ui_details
from report.pdf_report import generate_pdf_report

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/monitor', methods=['POST'])
def monitor():
    url = request.form.get('url')
    if not url:
        return "Error: URL not provided", 400

    # Collecting monitoring data
    performance_data = get_performance_metrics(url)
    security_data = {
        "csp": get_csp_components(url),
    }
    security_headers = get_security_headers(url)
    seo_data = get_seo_details(url)
    ui_data = get_ui_details(url)
    internal_links_data = get_internal_links(url)  # Add internal links data

    # Preparing results to send to the front end
    results = {
        "url": url,
        "performance": performance_data,
        "security": security_data,
        "seo": seo_data,
        "ui": ui_data,
        "security_headers": security_headers,
        "internal_links": internal_links_data,  # Include internal links data
    }
    return render_template('results.html', results=results)

@app.route('/export/pdf', methods=['POST'])
def export_pdf():
    results = request.json  # Get the results as JSON

    # Generate the PDF report and save it to the 'static/reports' folder
    pdf_filename = generate_pdf_report(results)
    pdf_path = os.path.join('static/reports', pdf_filename)

    # Check if the file was generated and exists
    if os.path.exists(pdf_path):
        return jsonify(pdf_path=pdf_path)  # Return the path to the PDF file as JSON
    else:
        return jsonify(error="Failed to generate PDF report."), 500

if __name__ == '__main__':
    app.run(debug=True)





# from flask import Flask, render_template, request, jsonify, send_from_directory
# import os
# from monitor.performance import get_performance_metrics, get_cdn_usage
# from monitor.security import get_ssl_certificate, get_http_headers
# from monitor.seo import get_seo_details
# from monitor.ui import get_ui_details
# from report.pdf_report import generate_pdf_report
#
# app = Flask(__name__)
# # app.config['UPLOAD_FOLDER'] = 'static/reports'  # Folder where you will store the PDFs
# #
# # # Ensure the 'reports' folder exists
# # os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/monitor', methods=['POST'])
# def monitor():
#     url = request.form.get('url')
#     if not url:
#         return "Error: URL not provided", 400
#
#     # Collecting monitoring data
#     performance_data = get_performance_metrics(url)
#
#     cdn_data = get_cdn_usage(url)
#
#     security_data = {
#         "ssl": get_ssl_certificate(url),
#         "headers": get_http_headers(url)
#     }
#     seo_data = get_seo_details(url)
#     ui_data = get_ui_details(url)
#
#     # Converting security headers to a normal dictionary (avoiding CaseInsensitiveDict)
#     security_data["headers"] = dict(security_data["headers"])
#
#     # Preparing results to send to the front end
#     results = {
#         "url": url,
#         "performance": performance_data,
#         "cdn": cdn_data,
#         "security": security_data,
#         "seo": seo_data,
#         "ui": ui_data
#     }
#     return render_template('results.html', results=results)
#
#
# @app.route('/export/pdf', methods=['POST'])
# def export_pdf():
#     results = request.json  # Get the results as JSON
#
#     # Generate the PDF report and save it to the 'static/reports' folder
#     pdf_filename = generate_pdf_report(results)
#     pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
#
#     # Check if the file was generated and exists
#     if os.path.exists(pdf_path):
#         return jsonify(pdf_path=pdf_path)  # Return the path to the PDF file as JSON
#     else:
#         return jsonify(error="Failed to generate PDF report."), 500
#
# 
# if __name__ == '__main__':
#     app.run(debug=True)
