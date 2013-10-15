#!/usr/bin/python

# This file is AUTO-GENERATED. Do not edit it directly, edit generator instead

import xcms_auth_add_new_user
import xcms_auth_change_user_by_admin
import xcms_auth_check_dup_email
import xcms_auth_check_dup_login
import xcms_auth_root_login
import xcms_auth_set_dup_email_by_admin
import xcms_content_add_page
import xcms_download_lectures
import xcms_metrics_check
import xcms_open_non_existing
import xcms_site_open_all_pages
import xcms_site_open_renamed_pages
import xcms_unittests
import xcms_version_check
import xcms_xsm_add_exams
import xcms_xsm_anketa_fill
import xcms_xsm_anketa_wrong_fill
import xcms_xsm_avatar

def getTests(baseUrl, args): return {
    "xcms_auth_add_new_user.py": xcms_auth_add_new_user.XcmsAuthAddNewUser(baseUrl, args),
    "xcms_auth_change_user_by_admin.py": xcms_auth_change_user_by_admin.XcmsAuthChangeUserByAdmin(baseUrl, args),
    "xcms_auth_check_dup_email.py": xcms_auth_check_dup_email.XcmsAuthCheckDupEmail(baseUrl, args),
    "xcms_auth_check_dup_login.py": xcms_auth_check_dup_login.XcmsAuthCheckDupLogin(baseUrl, args),
    "xcms_auth_root_login.py": xcms_auth_root_login.XcmsAuthRootLogin(baseUrl, args),
    "xcms_auth_set_dup_email_by_admin.py": xcms_auth_set_dup_email_by_admin.XcmsAuthSetDuplicateEmailByAdmin(baseUrl, args),
    "xcms_content_add_page.py": xcms_content_add_page.XcmsContentAddPage(baseUrl, args),
    "xcms_download_lectures.py": xcms_download_lectures.XcmsDownloadLectures(baseUrl, args),
    "xcms_metrics_check.py": xcms_metrics_check.XcmsMetricsCheck(baseUrl, args),
    "xcms_open_non_existing.py": xcms_open_non_existing.XcmsOpenNonExisting(baseUrl, args),
    "xcms_site_open_all_pages.py": xcms_site_open_all_pages.XcmsSiteOpenAllPages(baseUrl, args),
    "xcms_site_open_renamed_pages.py": xcms_site_open_renamed_pages.XcmsSiteOpenRenamedPages(baseUrl, args),
    "xcms_unittests.py": xcms_unittests.XcmsUnitTests(baseUrl, args),
    "xcms_version_check.py": xcms_version_check.XcmsVersionCheck(baseUrl, args),
    "xcms_xsm_add_exams.py": xcms_xsm_add_exams.XcmsXsmAddExams(baseUrl, args),
    "xcms_xsm_anketa_fill.py": xcms_xsm_anketa_fill.XcmsXsmAnketaFill(baseUrl, args),
    "xcms_xsm_anketa_wrong_fill.py": xcms_xsm_anketa_wrong_fill.XcmsXsmAnketaWrongFill(baseUrl, args),
    "xcms_xsm_avatar.py": xcms_xsm_avatar.XcmsXsmAvatar(baseUrl, args),
}
