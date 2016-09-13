# /automation/lib/

class Elements:
    """
    This Elements class contains temporary list of elements under uhone (for dtc type) and gethealthinsurance websites.
    """

    dict = {
        ################################################################################################
        # UnitedHealthOne elements
        ################################################################################################
        "zip_code_fld": ["#LocationViewModel_ZipCode"],
        "uhone_loading": ["div#loading-content.loading"],
        "applicant_gender_lst": ["select#PrimaryApplicant_Gender"],
        "applicant_dob_fld": ["#PrimaryApplicant_BirthDate"],
        "tobacco_use_fld": ["select#PrimaryApplicant_HasTobaccoUsage"],
        "view_plans_bttn": ["#hylViewPlans"],
        "quote_plan_page": ["#frmPlanList"],
        "plan": [".plans-list-result"],
        "term_life_ben_amt": [".quotePlanMaxLifetimeBenefit"],
        "policy_term": [".quotePlanMaxBenefitPeriod"],
        "add_to_cart": ["input.applyBtn"],
        "vision_and_more_bttn": [".tabiconANCILLARY "],
        "term_life_bttn": [".tabiconTERMLIFE"],
        "plan_name_lbl": [".plans-list-result", ".div25fL childAlignCenter", ".quotePlanDetails"],
        "term_life_benefit_amount_lbl": [".div20fL childAlignCenter", ".quotePlanMaxLifetimeBenefit",
                                         ".plans-text", "#RegularPlans_<sessionid?>_MaximumLifetimeBenefit"],
        "policy_term_lbl": [".div15fL childAlignCentert", ".quotePlanMaxBenefitPeriod", ".plans-text",
                            "#RegularPlans_<sessionid?>_MaximumBenefitPeriod"],
        "plan_cost_lbl": [".div20fL childAlignCenter plans-premium", ".quotePlanCost", ".planCost"],
        "expand_coverage_dlg": ["#expandYourCoverageModal .coverageModalContent"],
        "no_thanks_bttn": ["#expandYourCoverageModal a#anchorSkip"],
        "shopping_cart_page": [".brokerCensusHeader"],
        "apply_bttn": ["input[value=Apply]"],
        "applicant_info_page": ["#ctl00_lblPageTitle"],
        "firstname_fld": ["#ctl00_cphMain_txtPrimaryFirstName_txtPrimaryFirstNametxtMainInput"],
        "middlename_fld": ["#ctl00_cphMain_txtPrimaryMiddleName_txtPrimaryMiddleNametxtMainInput"],
        "lastname_fld": ["#ctl00_cphMain_txtPrimaryLastName_txtPrimaryLastNametxtMainInput"],
        "height_ft_lst": ["select#ctl00_cphMain_ddlPrimaryft_ddlPrimaryftddlMainInput"],
        "height_in_lst": ["select#ctl00_cphMain_ddlPrimaryin_ddlPrimaryinddlMainInput"],
        "weight_lbs_fld": ["#ctl00_cphMain_txtPrimaryWeight_txtPrimaryWeighttxtMainInput"],
        "physical_address_fld": [
            "#ctl00_cphMain_ucPrimaryPrimaryAddress_txtAddressLine1_txtAddressLine1txtMainInput"],
        "physical_city_fld": ["#ctl00_cphMain_ucPrimaryPrimaryAddress_txtCity_txtCitytxtMainInput"],
        "primary_home_area_fld": ["#ctl00_cphMain_txtPrimaryHome_txtPrimaryHomespcMainInputtxtAreaCode"],
        "primary_home_prefix_fld": ["#ctl00_cphMain_txtPrimaryHome_txtPrimaryHomespcMainInputtxtPrefix"],
        "primary_home_suffix_fld": ["#ctl00_cphMain_txtPrimaryHome_txtPrimaryHomespcMainInputtxtSuffix"],
        "email_address_fld": ["#ctl00_cphMain_txtPrimaryEmailAddress_txtPrimaryEmailAddresstxtMainInput"],
        "occupation_lst": ["select#ctl00_cphMain_ddlPrimaryOccupation_ddlPrimaryOccupationddlMainInput"],
        "continue_bttn": ["#ctl00_cphMain_NavigationMain1_btnSaveAndContinue"],
        "uhone_loading_2": ["#ctl00_cphMain_NavigationMain1_updateProgressDiv"],
        "before_you_continue_dlg": ["#ctl00_cphMain_NavigationMain1_ucRegistration_pnlRegistration"],
        "do_this_later_bttn": ["#ctl00_cphMain_NavigationMain1_ucRegistration_btnDoThisLater"],
        "term_life_questions_page": ["#ctl00_cphMain_QuestionWrapperUCOne_pnlApplicationQuestionUC"],
        "questions_all_no_rdbttn": ["input[type=radio][value=No]"],
        "questions_rdbttn": [
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl0_ParentQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1",
                "value:No"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl1_ParentQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl2_ParentQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl3_ParentQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl4_rSubQuestions_ctrl0_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl4_rSubQuestions_ctrl1_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl4_rSubQuestions_ctrl2_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl4_rSubQuestions_ctrl3_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl4_rSubQuestions_ctrl4_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl4_rSubQuestions_ctrl5_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl5_rSubQuestions_ctrl0_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl5_rSubQuestions_ctrl1_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl5_rSubQuestions_ctrl2_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl5_rSubQuestions_ctrl3_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl5_rSubQuestions_ctrl4_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl5_rSubQuestions_ctrl5_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl5_rSubQuestions_ctrl6_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl6_rSubQuestions_ctrl0_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl6_rSubQuestions_ctrl1_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl6_rSubQuestions_ctrl2_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl6_rSubQuestions_ctrl3_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl6_rSubQuestions_ctrl4_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl7_ParentQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl8_ParentQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl9_rSubQuestions_ctrl0_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl9_rSubQuestions_ctrl1_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl9_rSubQuestions_ctrl2_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl9_rSubQuestions_ctrl3_ChildQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl10_ParentQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl11_ParentQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"],
            [
                "#ctl00_cphMain_QuestionWrapperUCOne_rQuestions_ctrl12_ParentQuestionUC_rdoQuestionResponse_rdoQuestionResponserblMainInput_1"]],
        "payment_page": ["#ctl00_cphMain_divPayorSection"],
        "ini_pay_first_month_rdbttn": [
            "input[type=radio][id=ctl00_cphMain_PaymentDetailsUCSingle_rdoInitialPayment_rdoInitialPaymentrblMainInput_0]"],
        "ini_pay_credit_card_rdbttn": [
            "input[type=radio][id=ctl00_cphMain_PaymentDetailsUCSingle_rdoInitialPaymentMethod_rdoInitialPaymentMethodrblMainInput_1]"],
        "on_pay_monthly_rdbttn": [
            "input[type=radio][id=ctl00_cphMain_PaymentDetailsUCSingle_rdoOngoingPayment_rdoOngoingPaymentrblMainInput_0]"],
        "on_pay_credit_card_rdbttn": [
            "input[type=radio][id=ctl00_cphMain_PaymentDetailsUCSingle_rdoOngoingPaymentMethods_rdoOngoingPaymentMethodsrblMainInput_1]"],
        "cart_checkout_page": ["#ctl00_cphMain_pnlApplicationTypes"],
        "coverage_start_date_fld": [".dp-applied",
                                    "#ctl00_cphMain_ucTermLifeCriticalIllness_txtEffectiveDate_txtEffectiveDatetxtMainInput"],
        "credit_card_page": ["#ctl00_cphMain_ucCreditCardDetails_divCreditCard"],
        "credit_card_type_lst": [
            "select#ctl00_cphMain_ucCreditCardDetails_ddlCreditCardType_ddlCreditCardTypeddlMainInput"],
        "credit_card_num_fld": [
            "input#ctl00_cphMain_ucCreditCardDetails_txtCreditCardNumber_txtCreditCardNumbertxtMainInput"],
        "exp_date_month_lst": [
            "select#ctl00_cphMain_ucCreditCardDetails_ddlCardExpMonth_ddlCardExpMonthddlMainInput"],
        "exp_date_year_lst": [
            "select#ctl00_cphMain_ucCreditCardDetails_ddlCardExpYear_ddlCardExpYearddlMainInput"],
        "cardholder_zip_code_fld": [
            "#ctl00_cphMain_ucCreditCardDetails_txtCardZipCode_txtCardZipCodetxtMainInput"],
        "desired_withdrawal_lst": [
            "select#ctl00_cphMain_ucCreditCardDetails_ddlCreditCardDraftDay_ddlCreditCardDraftDayddlMainInput"],
        "save_application_bttn": ["#ctl00_cphMain_ucRegistrationModel_btnSaveandFinishLater"],
        "create_account_page": [".registration"],
        "user_id_fld": ["#UserId"],
        "password_fld": ["#Password"],
        "verify_password_fld": ["#VerifyPassword"],
        "email_address_reg_fld": ["#Email"],
        "verify_email_address_fld": ["#VerifyEmail"],
        "security_question_lst": ["select#SecurityQuestionId"],
        "security_question_fld": ["#SecurityQuestionAnswer"],
        "register_bttn": ["#btnRegister"],
        "esignature_page": ["#divReviewApplication"],
        "esignature_reviewed_chckbox": ["#ctl00_cphMain_chkAgree_chkAgreechkMainInput"],
        "esignature_electronic_chckbox": [
            "#ctl00_cphMain_chkCriticalIllnessReviewApplication_chkCriticalIllnessReviewApplicationchkMainInput"],
        "firstname_sig_fld": [
            "#ctl00_cphMain_ucPrimaryApplicantSignature_txtFirstName1_txtFirstName1txtMainInput"],
        "middlename_sig_fld": [
            "#ctl00_cphMain_ucPrimaryApplicantSignature_txtMiddleInitial1_txtMiddleInitial1txtMainInput"],
        "lastname_sig_fld": [
            "#ctl00_cphMain_ucPrimaryApplicantSignature_txtLastName1_txtLastName1txtMainInput"],
        "verify_firstname_fld": [
            "#ctl00_cphMain_ucPrimaryApplicantSignature_txtFirstName2_txtFirstName2txtMainInput"],
        "verify_middlename_fld": [
            "#ctl00_cphMain_ucPrimaryApplicantSignature_txtMiddleInitial2_txtMiddleInitial2txtMainInput"],
        "verify_lastname_fld": [
            "#ctl00_cphMain_ucPrimaryApplicantSignature_txtLastName2_txtLastName2txtMainInput"],
        "agree_bttn": ["#ctl00_cphMain_NavigationMain1_btnSaveAndContinue"],
        "thank_you_page": [".thank-maintitle"],

        ################################################################################################
        # GetHealthInsurance portion
        ################################################################################################
        "ghi_zip_code_fld": ["#zipCode"],
        "ghi_loading": ["div#ngplus-overlay-content.ngplus-overlay-content"],
        "ghi_applicant_gender_bttn": ["#primary_gender"],
        "ghi_applicant_dob_fld": ["#primary_birthday"],
        "ghi_coverage_start_date_fld": ["#coverageStartDate"],
        "ghi_view_plans_bttn": [".btn-primary"],
        "ghi_quote_plan_page": [".mc-planListPage"],
        "ghi_apply_bttn": [".mc-plan-list-item-actions", ".btn btn-primary mc-btn-fixed-sm"],
        "ghi_question_1of5_bttn": ["#defaultQuestion_13812_No"],
        "ghi_question_2of5_bttn": ["#defaultQuestion_13814_No"],
        "ghi_question_3of5_bttn": ["#defaultQuestion_13820_No"],
        "ghi_question_4of5_bttn": ["#defaultQuestion_13825_No"],
        "ghi_question_5of5_bttn": ["#defaultQuestion_13828_Yes"],
        "ghi_continue_bttn": ["input[value=Continue]"],
        "ghi_firstname_fld": ["#primary_firstName"],
        "ghi_lastname_fld": ["#primary_lastName"],
        "ghi_contact_info_address_fld": ["#contactInfo_address"],
        "ghi_contact_info_city_fld": ["#contactInfo_city"],
        "ghi_contact_info_phone_fld": ["#contactInfo_phoneNumber"],
        "ghi_contact_info_email_fld": ["#contactInfo_emailAddress"],
        "ghi_credit_card_fld": ["input[name=cardNumber]"],
        "ghi_cvv_fld": ["input[name=cvvCode]"],
        "ghi_firstname_billing_fld": ["#primary_firstName"],
        "ghi_lastname_billing_fld": ["#primary_lastName"],
        "ghi_exp_date_month_lst": ["select[name=month]"],
        "ghi_exp_date_year_lst": ["select[name=year]"],
        "ghi_billing_address_chckbox": ["#BillingAddress"]
    }

    def get_data(self, name):
        elements = False
        try:
            elements = self.dict[name][0]
        except KeyError:
            elements = False
        finally:
            return elements

# if __name__ == '__main__':
#    print "main"
