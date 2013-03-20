# This file is AUTO-GENERATED. Do not edit it directly, edit generator instead. 
 
import xcms_auth_add_new_user
import xcms_auth_check_dup_email
import xcms_auth_check_dup_login
import xcms_auth_root_login
import xcms_download_lectures
import xcms_metrics_check
import xcms_open_all_pages
import xcms_open_non_existing
import xcms_open_renamed_pages
import xcms_unittests
import xcms_version_check
import xcms_xsm_anketa_fill
import xcms_xsm_anketa_wrong_fill
def getTests(baseUrl, args): return [
xcms_auth_add_new_user.XcmsAuthAddNewUser(baseUrl, args),
xcms_auth_check_dup_email.XcmsAuthCheckDupEmail(baseUrl, args),
xcms_auth_check_dup_login.XcmsAuthCheckDupLogin(baseUrl, args),
xcms_auth_root_login.XcmsAuthRootLogin(baseUrl, args),
xcms_download_lectures.XcmsDownloadLectures(baseUrl, args),
xcms_metrics_check.XcmsMetricsCheck(baseUrl, args),
xcms_open_all_pages.XcmsOverallOpenPages(baseUrl, args),
xcms_open_non_existing.XcmsOpenNonExisting(baseUrl, args),
xcms_open_renamed_pages.XcmsOpenRenamedPages(baseUrl, args),
xcms_unittests.XcmsUnitTests(baseUrl, args),
xcms_version_check.XcmsVersionCheck(baseUrl, args),
xcms_xsm_anketa_fill.XcmsXsmAnketaFill(baseUrl, args),
xcms_xsm_anketa_wrong_fill.XcmsXsmAnketaWrongFill(baseUrl, args),
]

