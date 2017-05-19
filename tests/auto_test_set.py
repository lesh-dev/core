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
import xcms_auth_strange_usernames
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
import xcms_xsm_clear_forest_status
import xcms_xsm_course_mult_teachers
import xcms_xsm_hack_person_link
import xcms_xsm_link_user_profile
import xcms_xsm_list_filters
import xcms_xsm_phones


def get_tests(**kwargs):
    return [
        ("xcms_001_installer_default.py", xcms_001_installer_default.XcmsInstallerDefault(**kwargs)),
        ("xcms_auth_add_new_user.py", xcms_auth_add_new_user.XcmsAuthAddNewUser(**kwargs)),
        ("xcms_auth_cabinet_email_change.py", xcms_auth_cabinet_email_change.XcmsAuthCabinetEmailChange(**kwargs)),
        ("xcms_auth_change_user_by_admin.py", xcms_auth_change_user_by_admin.XcmsAuthChangeUserByAdmin(**kwargs)),
        ("xcms_auth_check_dup_email.py", xcms_auth_check_dup_email.XcmsAuthCheckDupEmail(**kwargs)),
        ("xcms_auth_check_dup_login.py", xcms_auth_check_dup_login.XcmsAuthCheckDupLogin(**kwargs)),
        ("xcms_auth_forgot_password.py", xcms_auth_forgot_password.XcmsAuthForgotPassword(**kwargs)),
        ("xcms_auth_root_login.py", xcms_auth_root_login.XcmsAuthRootLogin(**kwargs)),
        ("xcms_auth_set_dup_email_by_admin.py", xcms_auth_set_dup_email_by_admin.XcmsAuthSetDuplicateEmailByAdmin(**kwargs)),
        ("xcms_auth_strange_usernames.py", xcms_auth_strange_usernames.XcmsAuthStrangeUsernames(**kwargs)),
        ("xcms_content_add_page.py", xcms_content_add_page.XcmsContentAddPage(**kwargs)),
        ("xcms_content_auth_only_page.py", xcms_content_auth_only_page.XcmsContentAuthOnlyPage(**kwargs)),
        ("xcms_content_bad_path_page.py", xcms_content_bad_path_page.XcmsContentBadPathPage(**kwargs)),
        ("xcms_content_comment_processing.py", xcms_content_comment_processing.XcmsContentCommentProcessing(**kwargs)),
        ("xcms_content_contlists.py", xcms_content_contlists.XcmsContentContlist(**kwargs)),
        ("xcms_content_dollar_plugin.py", xcms_content_dollar_plugin.XcmsContentDollarPlugin(**kwargs)),
        ("xcms_content_hidden_page.py", xcms_content_hidden_page.XcmsContentHiddenPage(**kwargs)),
        ("xcms_content_nested_aliases.py", xcms_content_nested_aliases.XcmsContentNestedAliases(**kwargs)),
        ("xcms_content_nested_path.py", xcms_content_nested_path.XcmsContentNestedPathPage(**kwargs)),
        ("xcms_content_page_attachment.py", xcms_content_page_attachment.XcmsContentPageAttachment(**kwargs)),
        ("xcms_content_page_order.py", xcms_content_page_order.XcmsContentPageOrder(**kwargs)),
        ("xcms_content_remove_page.py", xcms_content_remove_page.XcmsContentRemovePage(**kwargs)),
        ("xcms_content_special_chars_page.py", xcms_content_special_chars_page.XcmsContentSpecialCharsPage(**kwargs)),
        ("xcms_content_top_level_page.py", xcms_content_top_level_page.XcmsContentTopLevelPage(**kwargs)),
        ("xcms_contest_submit_work.py", xcms_contest_submit_work.XcmsContestSubmitWork(**kwargs)),
        ("xcms_contest_submit_work_from_site.py", xcms_contest_submit_work_from_site.XcmsContestSubmitWorkFromSite(**kwargs)),
        ("xcms_download_lectures.py", xcms_download_lectures.XcmsDownloadLectures(**kwargs)),
        ("xcms_mailer_test_mailru.py", xcms_mailer_test_mailru.XcmsMailerTestMailRu(**kwargs)),
        ("xcms_metrics_check.py", xcms_metrics_check.XcmsMetricsCheck(**kwargs)),
        ("xcms_open_non_existing.py", xcms_open_non_existing.XcmsOpenNonExisting(**kwargs)),
        ("xcms_site_open_all_pages.py", xcms_site_open_all_pages.XcmsSiteOpenAllPages(**kwargs)),
        ("xcms_site_open_renamed_pages.py", xcms_site_open_renamed_pages.XcmsSiteOpenRenamedPages(**kwargs)),
        ("xcms_unittests.py", xcms_unittests.XcmsUnitTests(**kwargs)),
        ("xcms_version_check.py", xcms_version_check.XcmsVersionCheck(**kwargs)),
        ("xcms_warnings.py", xcms_warnings.XcmsWarnTest(**kwargs)),
        ("xcms_xsm_add_courses.py", xcms_xsm_add_courses.XcmsXsmAddCourses(**kwargs)),
        ("xcms_xsm_add_exams.py", xcms_xsm_add_exams.XcmsXsmAddExams(**kwargs)),
        ("xcms_xsm_add_person_to_school.py", xcms_xsm_add_person_to_school.XcmsXsmAddPersonToSchool(**kwargs)),
        ("xcms_xsm_add_school.py", xcms_xsm_add_school.XcmsXsmAddSchool(**kwargs)),
        ("xcms_xsm_anketa_dup_stress.py", xcms_xsm_anketa_dup_stress.XcmsXsmAnketaDupStress(**kwargs)),
        ("xcms_xsm_anketa_duplicate.py", xcms_xsm_anketa_duplicate.XcmsXsmAnketaDuplicate(**kwargs)),
        ("xcms_xsm_anketa_edit.py", xcms_xsm_anketa_edit.XcmsXsmAnketaEdit(**kwargs)),
        ("xcms_xsm_anketa_fill.py", xcms_xsm_anketa_fill.XcmsXsmAnketaFill(**kwargs)),
        ("xcms_xsm_anketa_wrong_fill.py", xcms_xsm_anketa_wrong_fill.XcmsXsmAnketaWrongFill(**kwargs)),
        ("xcms_xsm_avatar.py", xcms_xsm_avatar.XcmsXsmAvatar(**kwargs)),
        ("xcms_xsm_change_status_quick.py", xcms_xsm_change_status_quick.XcmsXsmChangeStatusQuick(**kwargs)),
        ("xcms_xsm_clear_forest_status.py", xcms_xsm_clear_forest_status.XcmsXsmClearForestStatus(**kwargs)),
        ("xcms_xsm_course_mult_teachers.py", xcms_xsm_course_mult_teachers.XcmsXsmCourseWithMultipleTeachers(**kwargs)),
        ("xcms_xsm_hack_person_link.py", xcms_xsm_hack_person_link.XcmsXsmHackPersonLink(**kwargs)),
        ("xcms_xsm_link_user_profile.py", xcms_xsm_link_user_profile.XcmsXsmLinkUserProfile(**kwargs)),
        ("xcms_xsm_list_filters.py", xcms_xsm_list_filters.XcmsXsmListFilters(**kwargs)),
        ("xcms_xsm_phones.py", xcms_xsm_phones.XcmsXsmPhones(**kwargs)),
    ]
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
import xcms_auth_strange_usernames
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
import xcms_xsm_add_person_to_school
import xcms_xsm_add_school
import xcms_xsm_anketa_dup_stress
import xcms_xsm_anketa_duplicate
import xcms_xsm_anketa_edit
import xcms_xsm_anketa_fill
import xcms_xsm_anketa_wrong_fill
import xcms_xsm_avatar
import xcms_xsm_change_status_quick
import xcms_xsm_clear_forest_status
import xcms_xsm_course_mult_teachers
import xcms_xsm_course_without_lecturer
import xcms_xsm_hack_person_link
import xcms_xsm_link_user_profile
import xcms_xsm_list_filters
import xcms_xsm_phones


def get_tests(**kwargs):
    return [
        ("xcms_001_installer_default.py", xcms_001_installer_default.XcmsInstallerDefault(**kwargs)),
        ("xcms_auth_add_new_user.py", xcms_auth_add_new_user.XcmsAuthAddNewUser(**kwargs)),
        ("xcms_auth_cabinet_email_change.py", xcms_auth_cabinet_email_change.XcmsAuthCabinetEmailChange(**kwargs)),
        ("xcms_auth_change_user_by_admin.py", xcms_auth_change_user_by_admin.XcmsAuthChangeUserByAdmin(**kwargs)),
        ("xcms_auth_check_dup_email.py", xcms_auth_check_dup_email.XcmsAuthCheckDupEmail(**kwargs)),
        ("xcms_auth_check_dup_login.py", xcms_auth_check_dup_login.XcmsAuthCheckDupLogin(**kwargs)),
        ("xcms_auth_forgot_password.py", xcms_auth_forgot_password.XcmsAuthForgotPassword(**kwargs)),
        ("xcms_auth_root_login.py", xcms_auth_root_login.XcmsAuthRootLogin(**kwargs)),
        ("xcms_auth_set_dup_email_by_admin.py", xcms_auth_set_dup_email_by_admin.XcmsAuthSetDuplicateEmailByAdmin(**kwargs)),
        ("xcms_auth_strange_usernames.py", xcms_auth_strange_usernames.XcmsAuthStrangeUsernames(**kwargs)),
        ("xcms_content_add_page.py", xcms_content_add_page.XcmsContentAddPage(**kwargs)),
        ("xcms_content_auth_only_page.py", xcms_content_auth_only_page.XcmsContentAuthOnlyPage(**kwargs)),
        ("xcms_content_bad_path_page.py", xcms_content_bad_path_page.XcmsContentBadPathPage(**kwargs)),
        ("xcms_content_comment_processing.py", xcms_content_comment_processing.XcmsContentCommentProcessing(**kwargs)),
        ("xcms_content_contlists.py", xcms_content_contlists.XcmsContentContlist(**kwargs)),
        ("xcms_content_dollar_plugin.py", xcms_content_dollar_plugin.XcmsContentDollarPlugin(**kwargs)),
        ("xcms_content_hidden_page.py", xcms_content_hidden_page.XcmsContentHiddenPage(**kwargs)),
        ("xcms_content_nested_aliases.py", xcms_content_nested_aliases.XcmsContentNestedAliases(**kwargs)),
        ("xcms_content_nested_path.py", xcms_content_nested_path.XcmsContentNestedPathPage(**kwargs)),
        ("xcms_content_page_attachment.py", xcms_content_page_attachment.XcmsContentPageAttachment(**kwargs)),
        ("xcms_content_page_order.py", xcms_content_page_order.XcmsContentPageOrder(**kwargs)),
        ("xcms_content_remove_page.py", xcms_content_remove_page.XcmsContentRemovePage(**kwargs)),
        ("xcms_content_special_chars_page.py", xcms_content_special_chars_page.XcmsContentSpecialCharsPage(**kwargs)),
        ("xcms_content_top_level_page.py", xcms_content_top_level_page.XcmsContentTopLevelPage(**kwargs)),
        ("xcms_contest_submit_work.py", xcms_contest_submit_work.XcmsContestSubmitWork(**kwargs)),
        ("xcms_contest_submit_work_from_site.py", xcms_contest_submit_work_from_site.XcmsContestSubmitWorkFromSite(**kwargs)),
        ("xcms_download_lectures.py", xcms_download_lectures.XcmsDownloadLectures(**kwargs)),
        ("xcms_mailer_test_mailru.py", xcms_mailer_test_mailru.XcmsMailerTestMailRu(**kwargs)),
        ("xcms_metrics_check.py", xcms_metrics_check.XcmsMetricsCheck(**kwargs)),
        ("xcms_open_non_existing.py", xcms_open_non_existing.XcmsOpenNonExisting(**kwargs)),
        ("xcms_site_open_all_pages.py", xcms_site_open_all_pages.XcmsSiteOpenAllPages(**kwargs)),
        ("xcms_site_open_renamed_pages.py", xcms_site_open_renamed_pages.XcmsSiteOpenRenamedPages(**kwargs)),
        ("xcms_unittests.py", xcms_unittests.XcmsUnitTests(**kwargs)),
        ("xcms_version_check.py", xcms_version_check.XcmsVersionCheck(**kwargs)),
        ("xcms_warnings.py", xcms_warnings.XcmsWarnTest(**kwargs)),
        ("xcms_xsm_add_courses.py", xcms_xsm_add_courses.XcmsXsmAddCourses(**kwargs)),
        ("xcms_xsm_add_exams.py", xcms_xsm_add_exams.XcmsXsmAddExams(**kwargs)),
        ("xcms_xsm_add_person_to_school.py", xcms_xsm_add_person_to_school.XcmsXsmAddPersonToSchool(**kwargs)),
        ("xcms_xsm_add_school.py", xcms_xsm_add_school.XcmsXsmAddSchool(**kwargs)),
        ("xcms_xsm_anketa_dup_stress.py", xcms_xsm_anketa_dup_stress.XcmsXsmAnketaDupStress(**kwargs)),
        ("xcms_xsm_anketa_duplicate.py", xcms_xsm_anketa_duplicate.XcmsXsmAnketaDuplicate(**kwargs)),
        ("xcms_xsm_anketa_edit.py", xcms_xsm_anketa_edit.XcmsXsmAnketaEdit(**kwargs)),
        ("xcms_xsm_anketa_fill.py", xcms_xsm_anketa_fill.XcmsXsmAnketaFill(**kwargs)),
        ("xcms_xsm_anketa_wrong_fill.py", xcms_xsm_anketa_wrong_fill.XcmsXsmAnketaWrongFill(**kwargs)),
        ("xcms_xsm_avatar.py", xcms_xsm_avatar.XcmsXsmAvatar(**kwargs)),
        ("xcms_xsm_change_status_quick.py", xcms_xsm_change_status_quick.XcmsXsmChangeStatusQuick(**kwargs)),
        ("xcms_xsm_clear_forest_status.py", xcms_xsm_clear_forest_status.XcmsXsmClearForestStatus(**kwargs)),
        ("xcms_xsm_course_mult_teachers.py", xcms_xsm_course_mult_teachers.XcmsXsmCourseWithMultipleTeachers(**kwargs)),
        ("xcms_xsm_course_without_lecturer.py", xcms_xsm_course_without_lecturer.XcmsXsmCourseWithoutLecturer(**kwargs)),
        ("xcms_xsm_hack_person_link.py", xcms_xsm_hack_person_link.XcmsXsmHackPersonLink(**kwargs)),
        ("xcms_xsm_link_user_profile.py", xcms_xsm_link_user_profile.XcmsXsmLinkUserProfile(**kwargs)),
        ("xcms_xsm_list_filters.py", xcms_xsm_list_filters.XcmsXsmListFilters(**kwargs)),
        ("xcms_xsm_phones.py", xcms_xsm_phones.XcmsXsmPhones(**kwargs)),
    ]
