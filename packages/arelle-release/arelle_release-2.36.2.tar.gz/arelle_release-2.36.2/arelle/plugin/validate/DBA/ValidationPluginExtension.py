"""
See COPYRIGHT.md for copyright information.
"""
from __future__ import annotations

from arelle.ModelValue import qname
from arelle.ValidateXbrl import ValidateXbrl
from arelle.typing import TypeGetText
from arelle.utils.validate.ValidationPlugin import ValidationPlugin
from .PluginValidationDataExtension import PluginValidationDataExtension

_: TypeGetText

DANISH_CURRENCY_ID = 'DKK'
NAMESPACE_ARR = 'http://xbrl.dcca.dk/arr'
NAMESPACE_CMN = 'http://xbrl.dcca.dk/cmn'
NAMESPACE_FSA = 'http://xbrl.dcca.dk/fsa'
NAMESPACE_GSD = 'http://xbrl.dcca.dk/gsd'
NAMESPACE_SOB = 'http://xbrl.dcca.dk/sob'
PERSONNEL_EXPENSE_THRESHOLD = 200000
ROUNDING_MARGIN = 1000


class ValidationPluginExtension(ValidationPlugin):
    def newPluginData(self, validateXbrl: ValidateXbrl) -> PluginValidationDataExtension:
        return PluginValidationDataExtension(
            self.name,
            annualReportTypes=frozenset([
                'Årsrapport',
                'årsrapport',
                'Annual report'
            ]),

            assetsQn=qname(f'{{{NAMESPACE_FSA}}}Assets'),
            auditedAssuranceReportsDanish='Andre erklæringer med sikkerhed',
            auditedAssuranceReportsEnglish='The independent auditor\'s reports (Other assurance Reports)',
            auditedExtendedReviewDanish='Erklæring om udvidet gennemgang',
            auditedExtendedReviewEnglish='Auditor\'s report on extended review',
            auditedFinancialStatementsDanish='Revisionspåtegning',
            auditedFinancialStatementsEnglish='Auditor\'s report on audited financial statements',
            averageNumberOfEmployeesQn=qname(f'{{{NAMESPACE_FSA}}}AverageNumberOfEmployees'),
            classOfReportingEntityQn=qname(f'{{{NAMESPACE_FSA}}}ClassOfReportingEntity'),
            consolidatedMemberQn=qname(f'{{{NAMESPACE_CMN}}}ConsolidatedMember'),
            consolidatedSoloDimensionQn=qname(f'{{{NAMESPACE_CMN}}}ConsolidatedSoloDimension'),
            dateOfApprovalOfAnnualReportQn=qname(f'{{{NAMESPACE_SOB}}}DateOfApprovalOfAnnualReport'),
            dateOfExtraordinaryDividendDistributedAfterEndOfReportingPeriod=qname(f'{{{NAMESPACE_FSA}}}DateOfExtraordinaryDividendDistributedAfterEndOfReportingPeriod'),
            dateOfGeneralMeetingQn=qname(f'{{{NAMESPACE_GSD}}}DateOfGeneralMeeting'),
            descriptionOfQualificationsOfAssuranceEngagementPerformedQn=qname(f'{{{NAMESPACE_ARR}}}DescriptionOfQualificationsOfAssuranceEngagementPerformed'),
            distributionOfResultsQns=frozenset([
                qname(f'{{{NAMESPACE_FSA}}}DistributionsResultDistribution'),
                qname(f'{{{NAMESPACE_FSA}}}ExtraordinaryDistributions'),
                qname(f'{{{NAMESPACE_FSA}}}ProposedDividendRecognisedInEquity'),
                qname(f'{{{NAMESPACE_FSA}}}ProposedExtraordinaryDividendRecognisedInEquity'),
                qname(f'{{{NAMESPACE_FSA}}}ProposedExtraordinaryDividendRecognisedInLiabilities'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredFromToHedgeFund'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredFromToReserveFund'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredFromToReservesAvailable'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredToFromEquityAttributableToParent'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredToFromMinorityInterests'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredToFromOtherStatutoryReserves'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredToFromReserveAccordingToArticlesOfAssociation'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredToFromReserveForNetRevaluationAccordingToEquityMethod'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredToFromReserveForNetRevaluationOfInvestmentAssets'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredToFromRestOfOtherReserves'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredToFromRetainedEarnings'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredToReserveForCurrentValueAdjustmentsOfCurrencyGains'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredToReserveForCurrentValueOfHedging'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredToReserveForDevelopmentExpenditure'),
                qname(f'{{{NAMESPACE_FSA}}}TransferredToReserveForEntrepreneurialCompany'),
            ]),
            employeeBenefitsExpenseQn=qname(f'{{{NAMESPACE_FSA}}}EmployeeBenefitsExpense'),
            equityQn=qname(f'{{{NAMESPACE_FSA}}}Equity'),
            extraordinaryCostsQn=qname(f'{{{NAMESPACE_FSA}}}ExtraordinaryCosts'),
            extraordinaryIncomeQn=qname(f'{{{NAMESPACE_FSA}}}ExtraordinaryIncome'),
            extraordinaryResultBeforeTaxQn=qname(f'{{{NAMESPACE_FSA}}}ExtraordinaryResultBeforeTax'),
            fr37RestrictedText='has not given rise to reservations',
            identificationNumberCvrOfAuditFirmQn=qname(f'{{{NAMESPACE_CMN}}}IdentificationNumberCvrOfAuditFirm'),
            independentAuditorsReportDanish='Den uafhængige revisors erklæringer (review)',
            independentAuditorsReportEnglish='The independent auditor\'s reports (Review)',
            informationOnTypeOfSubmittedReportQn=qname(f'{{{NAMESPACE_GSD}}}InformationOnTypeOfSubmittedReport'),
            liabilitiesQn=qname(f'{{{NAMESPACE_FSA}}}LiabilitiesAndEquity'),
            liabilitiesAndEquityQn=qname(f'{{{NAMESPACE_FSA}}}LiabilitiesAndEquity'),
            liabilitiesOtherThanProvisionsQn=qname(f'{{{NAMESPACE_FSA}}}LiabilitiesOtherThanProvisions'),
            longtermLiabilitiesOtherThanProvisionsQn=qname(f'{{{NAMESPACE_FSA}}}LongtermLiabilitiesOtherThanProvisions'),
            noncurrentAssetsQn=qname(f'{{{NAMESPACE_FSA}}}NoncurrentAssets'),
            nameAndSurnameOfChairmanOfGeneralMeetingQn=qname(f'{{{NAMESPACE_GSD}}}NameAndSurnameOfChairmanOfGeneralMeeting'),
            nameOfAuditFirmQn=qname(f'{{{NAMESPACE_CMN}}}NameOfAuditFirm'),
            positiveProfitThreshold=1000,
            precedingReportingPeriodEndDateQn=qname(f'{{{NAMESPACE_GSD}}}PredingReportingPeriodEndDate'),  # Typo in taxonomy
            precedingReportingPeriodStartDateQn=qname(f'{{{NAMESPACE_GSD}}}PrecedingReportingPeriodStartDate'),
            profitLossQn=qname(f'{{{NAMESPACE_FSA}}}ProfitLoss'),
            proposedDividendRecognisedInEquityQn=qname(f'{{{NAMESPACE_FSA}}}ProposedDividendRecognisedInEquity'),
            provisionsQn=qname(f'{{{NAMESPACE_FSA}}}Provisions'),
            reportingPeriodEndDateQn=qname(f'{{{NAMESPACE_GSD}}}ReportingPeriodEndDate'),
            reportingPeriodStartDateQn=qname(f'{{{NAMESPACE_GSD}}}ReportingPeriodStartDate'),
            shorttermLiabilitiesOtherThanProvisionsQn=qname(f'{{{NAMESPACE_FSA}}}ShorttermLiabilitiesOtherThanProvisions'),
            taxExpenseOnOrdinaryActivitiesQn=qname(f'{{{NAMESPACE_FSA}}}TaxExpenseOnOrdinaryActivities'),
            taxExpenseQn=qname(f'{{{NAMESPACE_FSA}}}TaxExpense'),
            typeOfAuditorAssistanceQn=qname(f'{{{NAMESPACE_CMN}}}TypeOfAuditorAssistance'),
            typeOfReportingPeriodDimensionQn=qname(f'{{{NAMESPACE_GSD}}}TypeOfReportingPeriodDimension'),
            wagesAndSalariesQn=qname(f'{{{NAMESPACE_FSA}}}WagesAndSalaries'),
        )
