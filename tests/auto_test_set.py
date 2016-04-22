#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is auto-generated

import xcms_001_installer_default
import xcms_auth_add_new_user
import xcms_auth_cabinet_email_change
import xcms_auth_change_user_by_admin
import xcms_auth_check_dup_email
import xcms_auth_check_dup_login
import xcms_auth_forgot_password
import xcms_auth_root_login
import xcms_auth_set_dup_email_by_admin
import xcms_content_add_page
import xcms_content_auth_only_page
import xcms_content_bad_path_page
import xcms_content_comment_processing
import xcms_content_contlists
import xcms_content_dollar_plugin
import xcms_content_hidden_page
import xcms_content_nested_aliases
import xcms_content_nested_path
import xcms_content_page_attachment
import xcms_content_page_order
import xcms_content_remove_page
import xcms_content_special_chars_page
import xcms_content_top_level_page
import xcms_contest_submit_work
import xcms_contest_submit_work_from_site
import xcms_download_lectures
import xcms_mailer_test_mailru
import xcms_metrics_check
import xcms_open_non_existing
import xcms_site_open_all_pages
import xcms_site_open_renamed_pages
import xcms_unittests
import xcms_version_check
import xcms_warnings
import xcms_xsm_add_courses
import xcms_xsm_add_exams
import xcms_xsm_add_school
import xcms_xsm_anketa_dup_stress
import xcms_xsm_anketa_duplicate
import xcms_xsm_anketa_edit
import xcms_xsm_anketa_fill
import xcms_xsm_anketa_wrong_fill
import xcms_xsm_avatar
import xcms_xsm_change_status_quick
import xcms_xsm_course_mult_teachers
import xcms_xsm_hack_person_link
import xcms_xsm_link_user_profile
import xcms_xsm_list_filters
import xcms_xsm_phones


def getTests(baseUrl, args):
    return [
        ("xcms_001_installer_default.py", xcms_001_installer_default.XcmsInstallerDefault(baseUrl, args)),
        ("xcms_auth_add_new_user.py", xcms_auth_add_new_user.XcmsAuthAddNewUser(baseUrl, args)),
        ("xcms_auth_cabinet_email_change.py", xcms_auth_cabinet_email_change.XcmsAuthCabinetEmailChange(baseUrl, args)),
        ("xcms_auth_change_user_by_admin.py", xcms_auth_change_user_by_admin.XcmsAuthChangeUserByAdmin(baseUrl, args)),
        ("xcms_auth_check_dup_email.py", xcms_auth_check_dup_email.XcmsAuthCheckDupEmail(baseUrl, args)),
        ("xcms_auth_check_dup_login.py", xcms_auth_check_dup_login.XcmsAuthCheckDupLogin(baseUrl, args)),
        ("xcms_auth_forgot_password.py", xcms_auth_forgot_password.XcmsAuthForgotPassword(baseUrl, args)),
        ("xcms_auth_root_login.py", xcms_auth_root_login.XcmsAuthRootLogin(baseUrl, args)),
        ("xcms_auth_set_dup_email_by_admin.py", xcms_auth_set_dup_email_by_admin.XcmsAuthSetDuplicateEmailByAdmin(baseUrl, args)),
        ("xcms_content_add_page.py", xcms_content_add_page.XcmsContentAddPage(baseUrl, args)),
        ("xcms_content_auth_only_page.py", xcms_content_auth_only_page.XcmsContentAuthOnlyPage(baseUrl, args)),
        ("xcms_content_bad_path_page.py", xcms_content_bad_path_page.XcmsContentBadPathPage(baseUrl, args)),
        ("xcms_content_comment_processing.py", xcms_content_comment_processing.XcmsContentCommentProcessing(baseUrl, args)),
        ("xcms_content_contlists.py", xcms_content_contlists.XcmsContentContlist(baseUrl, args)),
        ("xcms_content_dollar_plugin.py", xcms_content_dollar_plugin.XcmsContentDollarPlugin(baseUrl, args)),
        ("xcms_content_hidden_page.py", xcms_content_hidden_page.XcmsContentHiddenPage(baseUrl, args)),
        ("xcms_content_nested_aliases.py", xcms_content_nested_aliases.XcmsContentNestedAliases(baseUrl, args)),
        ("xcms_content_nested_path.py", xcms_content_nested_path.XcmsContentNestedPathPage(baseUrl, args)),
        ("xcms_content_page_attachment.py", xcms_content_page_attachment.XcmsContentPageAttachment(baseUrl, args)),
        ("xcms_content_page_order.py", xcms_content_page_order.XcmsContentPageOrder(baseUrl, args)),
        ("xcms_content_remove_page.py", xcms_content_remove_page.XcmsContentRemovePage(baseUrl, args)),
        ("xcms_content_special_chars_page.py", xcms_content_special_chars_page.XcmsContentSpecialCharsPage(baseUrl, args)),
        ("xcms_content_top_level_page.py", xcms_content_top_level_page.XcmsContentTopLevelPage(baseUrl, args)),
        ("xcms_contest_submit_work.py", xcms_contest_submit_work.XcmsContestSubmitWork(baseUrl, args)),
        ("xcms_contest_submit_work_from_site.py", xcms_contest_submit_work_from_site.XcmsContestSubmitWorkFromSite(baseUrl, args)),
        ("xcms_download_lectures.py", xcms_download_lectures.XcmsDownloadLectures(baseUrl, args)),
        ("xcms_mailer_test_mailru.py", xcms_mailer_test_mailru.XcmsMailerTestMailRu(baseUrl, args)),
        ("xcms_metrics_check.py", xcms_metrics_check.XcmsMetricsCheck(baseUrl, args)),
        ("xcms_open_non_existing.py", xcms_open_non_existing.XcmsOpenNonExisting(baseUrl, args)),
        ("xcms_site_open_all_pages.py", xcms_site_open_all_pages.XcmsSiteOpenAllPages(baseUrl, args)),
        ("xcms_site_open_renamed_pages.py", xcms_site_open_renamed_pages.XcmsSiteOpenRenamedPages(baseUrl, args)),
        ("xcms_unittests.py", xcms_unittests.XcmsUnitTests(baseUrl, args)),
        ("xcms_version_check.py", xcms_version_check.XcmsVersionCheck(baseUrl, args)),
        ("xcms_warnings.py", xcms_warnings.XcmsWarnTest(baseUrl, args)),
        ("xcms_xsm_add_courses.py", xcms_xsm_add_courses.XcmsXsmAddCourses(baseUrl, args)),
        ("xcms_xsm_add_exams.py", xcms_xsm_add_exams.XcmsXsmAddExams(baseUrl, args)),
        ("xcms_xsm_add_school.py", xcms_xsm_add_school.XcmsXsmAddSchool(baseUrl, args)),
        ("xcms_xsm_anketa_dup_stress.py", xcms_xsm_anketa_dup_stress.XcmsXsmAnketaDupStress(baseUrl, args)),
        ("xcms_xsm_anketa_duplicate.py", xcms_xsm_anketa_duplicate.XcmsXsmAnketaDuplicate(baseUrl, args)),
        ("xcms_xsm_anketa_edit.py", xcms_xsm_anketa_edit.XcmsXsmAnketaFill(baseUrl, args)),
        ("xcms_xsm_anketa_fill.py", xcms_xsm_anketa_fill.XcmsXsmAnketaFill(baseUrl, args)),
        ("xcms_xsm_anketa_wrong_fill.py", xcms_xsm_anketa_wrong_fill.XcmsXsmAnketaWrongFill(baseUrl, args)),
        ("xcms_xsm_avatar.py", xcms_xsm_avatar.XcmsXsmAvatar(baseUrl, args)),
        ("xcms_xsm_change_status_quick.py", xcms_xsm_change_status_quick.XcmsXsmChangeStatusQuick(baseUrl, args)),
        ("xcms_xsm_course_mult_teachers.py", xcms_xsm_course_mult_teachers.XcmsXsmCourseWithMultipleTeachers(baseUrl, args)),
        ("xcms_xsm_hack_person_link.py", xcms_xsm_hack_person_link.XcmsXsmHackPersonLink(baseUrl, args)),
        ("xcms_xsm_link_user_profile.py", xcms_xsm_link_user_profile.XcmsXsmLinkUserProfile(baseUrl, args)),
        ("xcms_xsm_list_filters.py", xcms_xsm_list_filters.XcmsXsmListFilters(baseUrl, args)),
        ("xcms_xsm_phones.py", xcms_xsm_phones.XcmsXsmPhones(baseUrl, args)),
    ]
