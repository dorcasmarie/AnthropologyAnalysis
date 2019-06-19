# coding: utf-8
from sqlalchemy import (
    BigInteger,
    Boolean,
    CHAR,
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    ForeignKey,
    types
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from SierraAccess import *


# Base = declarative_base()
Base = declarative_base(metadata=MetaData(schema="sierra_view"))
metadata = Base.metadata

"""
class BibRecordOrderRecordLink(Base):
    __tablename__ = "bib_record_order_record_link"
    #order_record_record_id = Column(Integer, ForeignKey("order_record.record_id"))
    #bib_record_record_id = Column(Integer, ForeignKey("bib_record.record_id"))
    bib_view_id = Column(Integer, ForeignKey("bib_view.id"), primary_key=True)
    order_view_id = Column(Integer, ForeignKey("order_view.id"), primary_key=True)
"""

class StrippedString(types.TypeDecorator):
    """
    Returns fund codes stripped of leading 0s

    """


    impl = types.String

    def process_bind_param(self, value, dialect):
        "No-op"
        return value


    def process_result_value(self, value, dialect):
        """
        Strip the trailing spaces on resulting values.
        If value is false, we return it as-is; it might be none
        for nullable columns
        """
        return value.lstrip("0") if value else value

    def copy(self):
        "Make a copy of this type"
        return StrippedString(self.impl.length)


bib_record_order_record_link = Table('bib_record_order_record_link', Base.metadata,
                                     Column('order_record_id', Integer, ForeignKey('order_record.id')),
                                     Column('bib_record_id', Integer, ForeignKey('bib_record.id')),
                                     )

class BibView(Base):
    __tablename__ = "bib_view"
    __table_args__ = {"schema": "sierra_view"}

    id = Column(BigInteger, ForeignKey('bib_record.id'), primary_key=True)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    language_code = Column(String(3))
    bcode1 = Column(CHAR(1))
    bcode2 = Column(String(3))
    bcode3 = Column(CHAR(1))
    country_code = Column(String(3))
    is_available_at_library = Column(Boolean)
    index_change_count = Column(Integer)
    allocation_rule_code = Column(CHAR(1))
    is_on_course_reserve = Column(Boolean)
    is_right_result_exact = Column(Boolean)
    skip_num = Column(Integer)
    cataloging_date_gmt = Column(DateTime(True))
    marc_type_code = Column(CHAR(1))
    title = Column(String(1000))
    record_creation_date_gmt = Column(DateTime(True))
    bib_record = relationship("BibRecord", back_populates="bib_view")
    #bib_record_id = Column(Integer, ForeignKey("bib_record.record_id"))

class BibRecord(Base):
    __tablename__ = "bib_record"
    __table_args__ = {"schema": "sierra_view"}

    id = Column(BigInteger)
    record_id = Column(BigInteger, primary_key=True)
    language_code = Column(String(3))
    bcode1 = Column(CHAR(1))
    bcode2 = Column(String(3))
    bcode3 = Column(CHAR(1))
    country_code = Column(String(3))
    index_change_count = Column(Integer)
    is_on_course_reserve = Column(Boolean)
    is_right_result_exact = Column(Boolean)
    allocation_rule_code = Column(CHAR(1))
    skip_num = Column(Integer)
    cataloging_date_gmt = Column(DateTime(True))
    marc_type_code = Column(CHAR(1))
    is_suppressed = Column(Boolean)
    bib_view = relationship("BibView", uselist=False, back_populates="bib_record")
    #order_records = relationship("OrderRecord", secondary=bib_record_order_record_link)
        #back_populates="bib_records")
    varfield_view = relationship("VarfieldView")  # has to be view not views
    record_metadata = relationship("RecordMetadatum")
    #order_views = relationship('OrderView', secondary='bib_record_order_record_link')
    order_records = relationship('OrderRecord', secondary=bib_record_order_record_link, back_populates ='bib_records')


class OrderRecord(Base):
    __tablename__ = "order_record"
    __table_args__ = {"schema": "sierra_view"}

    id = Column(BigInteger)
    record_id = Column(BigInteger, primary_key=True)
    accounting_unit_code_num = Column(Integer)
    acq_type_code = Column(CHAR(1))
    catalog_date_gmt = Column(DateTime(True))
    claim_action_code = Column(CHAR(1))
    ocode1 = Column(CHAR(1))
    ocode2 = Column(CHAR(1))
    ocode3 = Column(CHAR(1))
    ocode4 = Column(CHAR(1))
    estimated_price = Column(Numeric(30, 6))
    form_code = Column(CHAR(1))
    order_date_gmt = Column(DateTime(True))
    order_note_code = Column(CHAR(1))
    order_type_code = Column(CHAR(1))
    receiving_action_code = Column(CHAR(1))
    received_date_gmt = Column(DateTime(True))
    receiving_location_code = Column(String(3))
    billing_location_code = Column(String(3))
    order_status_code = Column(CHAR(1))
    temporary_location_code = Column(CHAR(1))
    vendor_record_code = Column(String(5))
    language_code = Column(String(3))
    blanket_purchase_order_num = Column(String(10000))
    country_code = Column(String(5))
    volume_count = Column(Integer)
    fund_allocation_rule_code = Column(CHAR(1))
    reopen_text = Column(String(255))
    list_price = Column(Numeric(30, 6))
    list_price_foreign_amt = Column(Numeric(30, 6))
    list_price_discount_amt = Column(Numeric(30, 6))
    list_price_service_charge = Column(Numeric(30, 6))
    is_suppressed = Column(Boolean)
    fund_copies_paid = Column(Integer)
    #bib_views = relationship("BibView", secondary="bib_record_order_record_link")
    bib_records = relationship("BibRecord", secondary=bib_record_order_record_link, back_populates = 'order_records')
    order_view = relationship("OrderView", uselist=False, back_populates="order_record")
    order_record_paid = relationship("OrderRecordPaid")
    order_record_cmf = relationship("OrderRecordCmf")


class OrderView(Base):
    __tablename__ = "order_view"
    __table_args__ = {"schema": "sierra_view"}

    id = Column(BigInteger, primary_key=True)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    record_id = Column(BigInteger, ForeignKey("order_record.id"), ForeignKey("order_record_cmf.order_record_id"))
    accounting_unit_code_num = Column(Integer)
    acq_type_code = Column(CHAR(1))
    catalog_date_gmt = Column(DateTime(True))
    claim_action_code = Column(CHAR(1))
    ocode1 = Column(CHAR(1))
    ocode2 = Column(CHAR(1))
    ocode3 = Column(CHAR(1))
    ocode4 = Column(CHAR(1))
    estimated_price = Column(Numeric(30, 6))
    material_type_code = Column(CHAR(1))
    order_date_gmt = Column(DateTime(True))
    order_note_code = Column(CHAR(1))
    order_type_code = Column(CHAR(1))
    receiving_action_code = Column(CHAR(1))
    received_date_gmt = Column(DateTime(True))
    receiving_location_code = Column(String(3))
    billing_location_code = Column(String(3))
    order_status_code = Column(CHAR(1))
    temporary_location_code = Column(CHAR(1))
    vendor_record_code = Column(String(5))
    language_code = Column(String(3))
    blanket_purchase_order_num = Column(String(10000))
    country_code = Column(String(5))
    volume_count = Column(Integer)
    fund_allocation_rule_code = Column(CHAR(1))
    reopen_text = Column(String(255))
    list_price = Column(Numeric(30, 6))
    list_price_foreign_amt = Column(Numeric(30, 6))
    list_price_discount_amt = Column(Numeric(30, 6))
    list_price_service_charge = Column(Numeric(30, 6))
    is_suppressed = Column(Boolean)
    record_creation_date_gmt = Column(DateTime(True))
    #order_record_id = Column(Integer, ForeignKey("order_record.id"))
    order_record = relationship("OrderRecord", back_populates="order_view", viewonly=True)
    order_record_cmf = relationship("OrderRecordCmf", lazy='joined')
    #bib_views = relationship("BibView", secondary="bib_record_order_record_link")

    def __init__(self, record_id=None, acq_type_code=None, order_status_code=None, ocode1=None):
        self.data = (record_id, acq_type_code, order_status_code, ocode1)

    def __repr__(self):
        return (self.record_id, self.acq_type_code, self.order_status_code, self.ocode1)


class VarfieldView(Base):
    __tablename__ = "varfield_view"
    __table_args__ = {"schema": "sierra_view"}

    id = Column(BigInteger, primary_key=True)
    # record_id = Column(BigInteger)
    record_id = Column(BigInteger, ForeignKey("bib_record.id"))
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    varfield_type_code = Column(CHAR(1))
    marc_tag = Column(String(3))
    marc_ind1 = Column(CHAR(1))
    marc_ind2 = Column(CHAR(1))
    occ_num = Column(Integer)
    field_content = Column(String(20001))
    bib_record = relationship("BibRecord", back_populates="varfield_view")
    # bib_record = Column(Integer, ForeignKey('bib_record.record_id'))


class RecordMetadatum(Base):
    __tablename__ = "record_metadata"
    __table_args__ = {"schema": "sierra_view"}

    id = Column(BigInteger, ForeignKey("bib_record.id"), ForeignKey("order_view.id"), primary_key=True)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    creation_date_gmt = Column(DateTime(True))
    deletion_date_gmt = Column(Date)
    campus_code = Column(String(5))
    agency_code_num = Column(SmallInteger)
    num_revisions = Column(Integer)
    record_last_updated_gmt = Column(DateTime(True))
    previous_last_updated_gmt = Column(DateTime(True))
    # bib_record = relationship("BibRecord")
    # bib_record_id = Column(Integer, ForeignKey('bib_record.record_id'))


class OrderRecordPaid(Base):
    __tablename__ = "order_record_paid"
    __table_args__ = {"schema": "sierra_view"}

    id = Column(BigInteger, primary_key=True)
    order_record_id = Column(BigInteger, ForeignKey("order_record.id"), ForeignKey("order_view.record_id"))
    display_order = Column(Integer)
    paid_date_gmt = Column(DateTime(True))
    paid_amount = Column(Float) #make to 2 demials
    foreign_paid_amount = Column(Numeric(30, 6))
    foreign_code = Column(String(10))
    voucher_num = Column(Integer)
    invoice_code = Column(String(20))
    invoice_date_gmt = Column(DateTime(True))
    from_date_gmt = Column(DateTime(True))
    to_date_gmt = Column(DateTime(True))
    copies = Column(Integer)
    note = Column(String(200))

    def __init__(self, paid_amount=None):
        self.data = (paid_amount)

    def __repr__(self):
        return (self.paid_amount)


class OrderRecordCmf(Base):
    __tablename__ = "order_record_cmf"
    __table_args__ = {"schema": "sierra_view"}

    id = Column(BigInteger, primary_key=True)
    order_record_id = Column(BigInteger, ForeignKey("order_record.id"))
    display_order = Column(Integer)
    fund_code = Column(StrippedString(100))
    copies = Column(Integer)
    location_code = Column(String(5))
    fund_master = relationship("FundMaster")
    order_view = relationship("OrderView", viewonly=True)

    def __init__(self, order_record_id=None, fund_code=None):
        self.data = (order_record_id, fund_code)

    def __repr__(self):
        return (self.order_record_id, self.fund_code)


class FundMaster(Base):
    __tablename__ = "fund_master"
    __table_args__ = {"schema": "sierra_view"}

    id = Column(Integer, primary_key=True)
    accounting_unit_id = Column(Integer, ForeignKey("accounting_unit.id"))
    code_num = Column(String, ForeignKey("order_record_cmf.fund_code"))
    code = Column(String)
    accounting_unit = relationship("AccountingUnit")
    order_record_cmf = relationship("OrderRecordCmf")


class AccountingUnit(Base):
    __tablename__ = "accounting_unit"
    __table_args__ = {"schema": "sierra_view"}

    id = Column(Integer, primary_key=True)
    code_num = Column(String)
    fund_master = relationship("FundMaster")

connection = SierraAccess().connect()

"""
result = connection.query(OrderRecord).first()
print(result.order_record_cmf[0].id)

res = connection.query(OrderRecordCmf).first()
print(res.fund_master[0].id)
"""



class AccountingTransaction(Base):
    __tablename__ = 'accounting_transaction'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    accounting_unit_id = Column(Integer)
    fund_master_id = Column(Integer)
    voucher_num = Column(Integer)
    voucher_seq_num = Column(Integer)
    posted_date = Column(DateTime(True))
    amt_type = Column(Integer)
    amt = Column(Numeric(30, 6))
    note = Column(String(255))
    source_name = Column(String(50))
    last_updated_gmt = Column(DateTime(True))


class AccountingTransactionIllExpenditure(Base):
    __tablename__ = 'accounting_transaction_ill_expenditure'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    accounting_transaction_id = Column(Integer)


class AccountingTransactionInvoiceEncumbrance(Base):
    __tablename__ = 'accounting_transaction_invoice_encumbrance'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    accounting_transaction_id = Column(Integer)
    invoice_record_metadata_id = Column(BigInteger)
    invoice_date = Column(DateTime(True))
    order_record_metadata_id = Column(BigInteger)
    bib_record_metadata_id = Column(BigInteger)
    location_code = Column(String(255))
    copies = Column(Integer)
    foreign_currency_code = Column(String(20))
    foreign_currency_amt = Column(Numeric(30, 6))
    xy_note = Column(String(255))
    subscription_from_date = Column(DateTime(True))
    subscription_to_date = Column(DateTime(True))
    invoice_record_line_item_num = Column(Integer)
    vendor_record_metadata_id = Column(BigInteger)


class AccountingTransactionInvoiceExpenditure(Base):
    __tablename__ = 'accounting_transaction_invoice_expenditure'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    accounting_transaction_id = Column(Integer)
    invoice_record_metadata_id = Column(BigInteger)
    invoice_date = Column(DateTime(True))
    order_record_metadata_id = Column(BigInteger)
    bib_record_metadata_id = Column(BigInteger)
    subfund_code = Column(String(20))
    location_code = Column(String(20))
    copies = Column(Integer)
    tax_amt = Column(Numeric(30, 6))
    foreign_currency_code = Column(String(20))
    foreign_currency_amt = Column(Numeric(30, 6))
    foreign_currency_tax_amt = Column(Numeric(30, 6))
    xy_note = Column(String(255))
    use_tax_amt = Column(Numeric(30, 6))
    ship_amt = Column(Numeric(30, 6))
    discount_amt = Column(Numeric(30, 6))
    service_charge_amt = Column(Numeric(30, 6))
    subscription_from_date = Column(DateTime(True))
    subscription_to_date = Column(DateTime(True))
    invoice_record_line_item_num = Column(Integer)
    vendor_record_metadata_id = Column(BigInteger)


class AccountingTransactionManualAppropriation(Base):
    __tablename__ = 'accounting_transaction_manual_appropriation'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    accounting_transaction_id = Column(Integer)


class AccountingTransactionManualEncumbrance(Base):
    __tablename__ = 'accounting_transaction_manual_encumbrance'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    accounting_transaction_id = Column(Integer)


class AccountingTransactionManualExpenditure(Base):
    __tablename__ = 'accounting_transaction_manual_expenditure'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    accounting_transaction_id = Column(Integer)


class AccountingTransactionOrderCancellation(Base):
    __tablename__ = 'accounting_transaction_order_cancellation'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    accounting_transaction_id = Column(Integer)
    order_record_metadata_id = Column(BigInteger)
    bib_record_metadata_id = Column(BigInteger)
    location_code = Column(String(20))
    copies = Column(Integer)
    foreign_currency_code = Column(String(20))
    foreign_currency_amt = Column(Numeric(30, 6))
    subscription_from_date = Column(DateTime(True))
    subscription_to_date = Column(DateTime(True))
    vendor_record_metadata_id = Column(BigInteger)


class AccountingTransactionOrderEncumbrance(Base):
    __tablename__ = 'accounting_transaction_order_encumbrance'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    accounting_transaction_id = Column(Integer)
    order_record_metadata_id = Column(BigInteger)
    bib_record_metadata_id = Column(BigInteger)
    location_code = Column(String(20))
    copies = Column(Integer)
    foreign_currency_code = Column(String(20))
    foreign_currency_amt = Column(Numeric(30, 6))
    subscription_from_date = Column(DateTime(True))
    subscription_to_date = Column(DateTime(True))
    vendor_record_metadata_id = Column(BigInteger)





class AccountingUnitMyuser(Base):
    __tablename__ = 'accounting_unit_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(Integer)
    name = Column(String(20))


class AccountingUnitName(Base):
    __tablename__ = 'accounting_unit_name'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    iii_language_id = Column(BigInteger)
    accounting_unit_id = Column(BigInteger)
    name = Column(String(20))


class AcqTypeProperty(Base):
    __tablename__ = 'acq_type_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)


class AcqTypePropertyMyuser(Base):
    __tablename__ = 'acq_type_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    name = Column(String(255))


class AcqTypePropertyName(Base):
    __tablename__ = 'acq_type_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    acq_type_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class AgencyProperty(Base):
    __tablename__ = 'agency_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code_num = Column(Integer)
    display_order = Column(Integer)


class AgencyPropertyLocationGroup(Base):
    __tablename__ = 'agency_property_location_group'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    agency_property_code_num = Column(Integer)
    location_group_port_number = Column(Integer)


class AgencyPropertyMyuser(Base):
    __tablename__ = 'agency_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class AgencyPropertyName(Base):
    __tablename__ = 'agency_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    agency_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class AuthorityRecord(Base):
    __tablename__ = 'authority_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    marc_type_code = Column(CHAR(1))
    code1 = Column(CHAR(1))
    code2 = Column(CHAR(1))
    suppress_code = Column(CHAR(1))
    is_suppressed = Column(Boolean)


class AuthorityView(Base):
    __tablename__ = 'authority_view'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    marc_type_code = Column(CHAR(1))
    code1 = Column(CHAR(1))
    code2 = Column(CHAR(1))
    suppress_code = Column(CHAR(1))
    record_creation_date_gmt = Column(DateTime(True))


class B2mCategory(Base):
    __tablename__ = 'b2m_category'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    code = Column(String(20))
    is_staff_enabled = Column(Boolean)


class B2mCategoryMyuser(Base):
    __tablename__ = 'b2m_category_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(20))
    is_staff_enabled = Column(Boolean)
    name = Column(String(60))


class B2mCategoryName(Base):
    __tablename__ = 'b2m_category_name'
    __table_args__ = {'schema': 'sierra_view'}

    b2m_category_id = Column(BigInteger)
    iii_language_id = Column(BigInteger)
    name = Column(String(60))


class BackupAdmin(Base):
    __tablename__ = 'backup_admin'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    name = Column(String(128))
    email = Column(String(128))


class BibLevelProperty(Base):
    __tablename__ = 'bib_level_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)


class BibLevelPropertyMyuser(Base):
    __tablename__ = 'bib_level_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    name = Column(String(255))


class BibLevelPropertyName(Base):
    __tablename__ = 'bib_level_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    bib_level_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))





class BibRecordCallNumberPrefix(Base):
    __tablename__ = 'bib_record_call_number_prefix'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    bib_record_id = Column(BigInteger)
    call_number_prefix = Column(String(10))


class BibRecordHoldingRecordLink(Base):
    __tablename__ = 'bib_record_holding_record_link'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    bib_record_id = Column(BigInteger)
    holding_record_id = Column(BigInteger)
    holdings_display_order = Column(Integer)


class BibRecordItemRecordLink(Base):
    __tablename__ = 'bib_record_item_record_link'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    bib_record_id = Column(BigInteger)
    item_record_id = Column(BigInteger)
    items_display_order = Column(Integer)
    bibs_display_order = Column(Integer)


class BibRecordLocation(Base):
    __tablename__ = 'bib_record_location'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    bib_record_id = Column(BigInteger)
    copies = Column(Integer)
    location_code = Column(String(5))
    display_order = Column(Integer)





class BibRecordProperty(Base):
    __tablename__ = 'bib_record_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    bib_record_id = Column(BigInteger)
    best_title = Column(String(1000))
    bib_level_code = Column(String(3))
    material_code = Column(String(3))
    publish_year = Column(Integer)
    best_title_norm = Column(String(1000))
    best_author = Column(String(1000))
    best_author_norm = Column(String(1000))


class BibRecordVolumeRecordLink(Base):
    __tablename__ = 'bib_record_volume_record_link'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    bib_record_id = Column(BigInteger)
    volume_record_id = Column(BigInteger)
    volumes_display_order = Column(Integer)




class BillingLocationProperty(Base):
    __tablename__ = 'billing_location_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(CHAR(1))
    display_order = Column(Integer)


class BillingLocationPropertyMyuser(Base):
    __tablename__ = 'billing_location_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(CHAR(1))
    display_order = Column(Integer)
    name = Column(String(255))


class BillingLocationPropertyName(Base):
    __tablename__ = 'billing_location_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    billing_location_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class Booking(Base):
    __tablename__ = 'booking'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    item_record_id = Column(BigInteger)
    patron_record_id = Column(BigInteger)
    created_gmt = Column(DateTime(True))
    start_gmt = Column(DateTime(True))
    end_gmt = Column(DateTime(True))
    type_code = Column(CHAR(1))
    prep_period = Column(Integer)
    location_code = Column(String(5))
    delivery_code = Column(SmallInteger)
    location_note = Column(String(19))
    note = Column(String(1000))
    event_name = Column(String(1000))


class BoolInfo(Base):
    __tablename__ = 'bool_info'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    name = Column(String(512))
    max = Column(Integer)
    count = Column(Integer)
    record_type_code = Column(CHAR(1))
    record_range = Column(String(512))
    bool_gmt = Column(DateTime(True))
    bool_query = Column(Text)
    sql_query = Column(Text)
    is_lookup_call = Column(Boolean)
    is_lookup_880 = Column(Boolean)
    is_search_holdings = Column(Boolean)
    sorter_spec = Column(Text)
    lister_spec = Column(Text)
    status_code = Column(CHAR(1))
    iii_user_name = Column(String(255))
    list_export_spec = Column(Text)
    owner_iii_user_name = Column(String(255))
    is_store_field = Column(Boolean)
    is_card_search = Column(Boolean)


class BoolSet(Base):
    __tablename__ = 'bool_set'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_metadata_id = Column(BigInteger)
    bool_info_id = Column(BigInteger)
    display_order = Column(Integer)
    field_key = Column(String(255))
    occ_num = Column(Integer)


class Branch(Base):
    __tablename__ = 'branch'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    address = Column(String(300))
    email_source = Column(String(255))
    email_reply_to = Column(String(255))
    address_latitude = Column(String(32))
    address_longitude = Column(String(32))
    code_num = Column(Integer)


class BranchChange(Base):
    __tablename__ = 'branch_change'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    branch_code_num = Column(Integer)
    description = Column(String(1000))


class BranchMyuser(Base):
    __tablename__ = 'branch_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(Integer)
    address = Column(String(300))
    email_source = Column(String(255))
    email_reply_to = Column(String(255))
    address_latitude = Column(String(32))
    address_longitude = Column(String(32))
    name = Column(String(255))


class BranchName(Base):
    __tablename__ = 'branch_name'
    __table_args__ = {'schema': 'sierra_view'}

    branch_id = Column(Integer)
    name = Column(String(255))
    iii_language_id = Column(Integer)


class Catmaint(Base):
    __tablename__ = 'catmaint'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    is_locked = Column(Boolean)
    is_viewed = Column(Boolean)
    condition_code_num = Column(Integer)
    index_tag = Column(CHAR(1))
    index_entry = Column(Text)
    record_metadata_id = Column(BigInteger)
    statistics_group_code_num = Column(Integer)
    process_gmt = Column(DateTime(True))
    program_code = Column(String(255))
    iii_user_name = Column(String(255))
    one_xx_entry = Column(Text)
    authority_record_metadata_id = Column(BigInteger)
    old_field = Column(Text)
    new_240_field = Column(Text)
    field = Column(Text)
    cataloging_date_gmt = Column(DateTime(True))
    index_prev = Column(Text)
    index_next = Column(Text)
    correct_heading = Column(Text)
    author = Column(Text)
    title = Column(Text)
    phrase_entry_id = Column(BigInteger)


class Checkout(Base):
    __tablename__ = 'checkout'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    patron_record_id = Column(BigInteger)
    item_record_id = Column(BigInteger)
    items_display_order = Column(Integer)
    due_gmt = Column(DateTime(True))
    loanrule_code_num = Column(Integer)
    checkout_gmt = Column(DateTime(True))
    renewal_count = Column(Integer)
    overdue_count = Column(Integer)
    overdue_gmt = Column(DateTime(True))
    recall_gmt = Column(DateTime(True))
    ptype = Column(SmallInteger)


class CircTran(Base):
    __tablename__ = 'circ_trans'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    transaction_gmt = Column(DateTime(True))
    application_name = Column(String(256))
    source_code = Column(String(256))
    op_code = Column(String(256))
    patron_record_id = Column(BigInteger)
    item_record_id = Column(BigInteger)
    volume_record_id = Column(BigInteger)
    bib_record_id = Column(BigInteger)
    stat_group_code_num = Column(Integer)
    due_date_gmt = Column(DateTime(True))
    count_type_code_num = Column(Integer)
    itype_code_num = Column(Integer)
    icode1 = Column(Integer)
    icode2 = Column(String(10))
    item_location_code = Column(String(5))
    item_agency_code_num = Column(Integer)
    ptype_code = Column(String(6))
    pcode1 = Column(CHAR(1))
    pcode2 = Column(CHAR(1))
    pcode3 = Column(Integer)
    pcode4 = Column(Integer)
    patron_home_library_code = Column(String(5))
    patron_agency_code_num = Column(Integer)
    loanrule_code_num = Column(Integer)


class ClaimActionProperty(Base):
    __tablename__ = 'claim_action_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)


class ClaimActionPropertyMyuser(Base):
    __tablename__ = 'claim_action_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    name = Column(String(255))


class ClaimActionPropertyName(Base):
    __tablename__ = 'claim_action_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    claim_action_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class ColagencyCriteriaHomeLibrary(Base):
    __tablename__ = 'colagency_criteria_home_libraries'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    colagency_id = Column(BigInteger)
    home_library = Column(String(5))


class ColagencyCriteriaPtype(Base):
    __tablename__ = 'colagency_criteria_ptypes'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    colagency_id = Column(BigInteger)
    ptype = Column(SmallInteger)


class ColagencyPatron(Base):
    __tablename__ = 'colagency_patron'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    patron_record_metadata_id = Column(BigInteger)
    status = Column(String(15))
    time_removed_gmt = Column(DateTime(True))
    time_report_last_run_gmt = Column(DateTime(True))
    colagency_criteria_metadata_id = Column(BigInteger)


class Collection(Base):
    __tablename__ = 'collection'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    is_default = Column(Boolean)
    display_order = Column(Integer)
    avg_width = Column(Float)
    avg_cost = Column(Numeric(30, 6))


class CollectionMyuser(Base):
    __tablename__ = 'collection_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    is_default = Column(Boolean)
    display_order = Column(Integer)
    name = Column(String(255))


class ContactRecord(Base):
    __tablename__ = 'contact_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    code = Column(String(5))
    is_suppressed = Column(Boolean)


class ContactRecordAddressType(Base):
    __tablename__ = 'contact_record_address_type'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    code = Column(CHAR(1))


class ContactView(Base):
    __tablename__ = 'contact_view'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    code = Column(String(5))
    record_creation_date_gmt = Column(DateTime(True))
    is_suppressed = Column(Boolean)


class ControlField(Base):
    __tablename__ = 'control_field'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    varfield_type_code = Column(CHAR(1))
    control_num = Column(Integer)
    p00 = Column(CHAR(1))
    p01 = Column(CHAR(1))
    p02 = Column(CHAR(1))
    p03 = Column(CHAR(1))
    p04 = Column(CHAR(1))
    p05 = Column(CHAR(1))
    p06 = Column(CHAR(1))
    p07 = Column(CHAR(1))
    p08 = Column(CHAR(1))
    p09 = Column(CHAR(1))
    p10 = Column(CHAR(1))
    p11 = Column(CHAR(1))
    p12 = Column(CHAR(1))
    p13 = Column(CHAR(1))
    p14 = Column(CHAR(1))
    p15 = Column(CHAR(1))
    p16 = Column(CHAR(1))
    p17 = Column(CHAR(1))
    p18 = Column(CHAR(1))
    p19 = Column(CHAR(1))
    p20 = Column(CHAR(1))
    p21 = Column(CHAR(1))
    p22 = Column(CHAR(1))
    p23 = Column(CHAR(1))
    p24 = Column(CHAR(1))
    p25 = Column(CHAR(1))
    p26 = Column(CHAR(1))
    p27 = Column(CHAR(1))
    p28 = Column(CHAR(1))
    p29 = Column(CHAR(1))
    p30 = Column(CHAR(1))
    p31 = Column(CHAR(1))
    p32 = Column(CHAR(1))
    p33 = Column(CHAR(1))
    p34 = Column(CHAR(1))
    p35 = Column(CHAR(1))
    p36 = Column(CHAR(1))
    p37 = Column(CHAR(1))
    p38 = Column(CHAR(1))
    p39 = Column(CHAR(1))
    p40 = Column(CHAR(1))
    p41 = Column(CHAR(1))
    p42 = Column(CHAR(1))
    p43 = Column(CHAR(1))
    occ_num = Column(Integer)
    remainder = Column(String(100))


class Counter(Base):
    __tablename__ = 'counter'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(100))
    num = Column(Integer)


class CountryProperty(Base):
    __tablename__ = 'country_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)


class CountryPropertyMyuser(Base):
    __tablename__ = 'country_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    name = Column(String(255))


class CountryPropertyName(Base):
    __tablename__ = 'country_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    country_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class CourseRecord(Base):
    __tablename__ = 'course_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    begin_date = Column(DateTime(True))
    end_date = Column(DateTime(True))
    location_code = Column(String(5))
    ccode1 = Column(String(20))
    ccode2 = Column(String(20))
    ccode3 = Column(String(20))
    is_suppressed = Column(Boolean)


class CourseRecordBibRecordLink(Base):
    __tablename__ = 'course_record_bib_record_link'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    course_record_id = Column(BigInteger)
    bib_record_id = Column(BigInteger)
    status_change_date = Column(DateTime(True))
    status_code = Column(String(5))
    bibs_display_order = Column(Integer)


class CourseRecordItemRecordLink(Base):
    __tablename__ = 'course_record_item_record_link'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    course_record_id = Column(BigInteger)
    item_record_id = Column(BigInteger)
    status_change_date = Column(DateTime(True))
    status_code = Column(String(5))
    items_display_order = Column(Integer)


class CourseView(Base):
    __tablename__ = 'course_view'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    begin_date = Column(DateTime(True))
    end_date = Column(DateTime(True))
    location_code = Column(String(5))
    ccode1 = Column(String(20))
    ccode2 = Column(String(20))
    ccode3 = Column(String(20))
    record_creation_date_gmt = Column(DateTime(True))


class DarcServiceView(Base):
    __tablename__ = 'darc_service_view'
    __table_args__ = {'schema': 'sierra_view'}

    group_name = Column(String(30))
    service_name = Column(String(30))
    param = Column(String(30))
    value = Column(String(255))


class DiacriticCategory(Base):
    __tablename__ = 'diacritic_category'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    name = Column(String(255))
    is_unicode_style = Column(Boolean)
    is_big5 = Column(Boolean)
    is_cccii = Column(Boolean)
    is_eacc = Column(Boolean)
    is_thai = Column(Boolean)
    is_winpage = Column(Boolean)
    is_multibyte = Column(Boolean)
    is_decomposed_character_used = Column(Boolean)
    is_general_rule_enabled = Column(Boolean)
    is_staff_enabled = Column(Boolean)


class DiacriticMapping(Base):
    __tablename__ = 'diacritic_mapping'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    diacritic = Column(String(255))
    letter = Column(CHAR(1))
    description = Column(String(255))
    mapped_string = Column(String(255))
    is_preferred = Column(Boolean)
    diacritic_category_id = Column(Integer)
    width = Column(Integer)
    display_order = Column(Integer)


class EadHierarchy(Base):
    __tablename__ = 'ead_hierarchy'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    bib_record_id = Column(BigInteger)
    entry = Column(String(300))


class ExternalFundProperty(Base):
    __tablename__ = 'external_fund_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    accounting_unit_id = Column(Integer)
    code_num = Column(Integer)


class ExternalFundPropertyMyuser(Base):
    __tablename__ = 'external_fund_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(Integer)
    accounting_unit_id = Column(Integer)
    name = Column(String(255))


class ExternalFundPropertyName(Base):
    __tablename__ = 'external_fund_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    external_fund_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class Fine(Base):
    __tablename__ = 'fine'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    patron_record_id = Column(BigInteger)
    assessed_gmt = Column(DateTime(True))
    invoice_num = Column(Integer)
    item_charge_amt = Column(Numeric(30, 6))
    processing_fee_amt = Column(Numeric(30, 6))
    billing_fee_amt = Column(Numeric(30, 6))
    charge_code = Column(CHAR(1))
    charge_location_code = Column(String(5))
    paid_gmt = Column(DateTime(True))
    terminal_num = Column(Integer)
    paid_amt = Column(Numeric(30, 6))
    initials = Column(String(12))
    created_code = Column(CHAR(1))
    is_print_bill = Column(Boolean)
    description = Column(String(100))
    item_record_metadata_id = Column(BigInteger)
    checkout_gmt = Column(DateTime(True))
    due_gmt = Column(DateTime(True))
    returned_gmt = Column(DateTime(True))
    loanrule_code_num = Column(Integer)
    title = Column(String(82))
    original_patron_record_metadata_id = Column(BigInteger)
    original_transfer_gmt = Column(DateTime(True))
    previous_invoice_num = Column(Integer)
    display_order = Column(Integer)


class FinesPaid(Base):
    __tablename__ = 'fines_paid'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    fine_assessed_date_gmt = Column(DateTime(True))
    patron_record_metadata_id = Column(BigInteger)
    item_charge_amt = Column(Numeric(30, 6))
    processing_fee_amt = Column(Numeric(30, 6))
    billing_fee_amt = Column(Numeric(30, 6))
    charge_type_code = Column(CHAR(1))
    charge_location_code = Column(String(5))
    paid_date_gmt = Column(DateTime(True))
    tty_num = Column(Integer)
    last_paid_amt = Column(Numeric(30, 6))
    iii_user_name = Column(String(255))
    fine_creation_mode_code = Column(CHAR(1))
    print_bill_code = Column(CHAR(1))
    item_record_metadata_id = Column(BigInteger)
    checked_out_date_gmt = Column(DateTime(True))
    due_date_gmt = Column(DateTime(True))
    returned_date_gmt = Column(DateTime(True))
    loan_rule_code_num = Column(Integer)
    description = Column(String(100))
    paid_now_amt = Column(Numeric(30, 6))
    payment_status_code = Column(CHAR(1))
    payment_type_code = Column(CHAR(1))
    payment_note = Column(String(150))
    transaction_id = Column(Integer)
    invoice_num = Column(Integer)
    old_invoice_num = Column(Integer)


class FirmProperty(Base):
    __tablename__ = 'firm_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(5))
    category_code = Column(String(1))
    contact_name = Column(String(255))
    contact_addr1 = Column(String(255))
    contact_addr2 = Column(String(255))
    contact_addr3 = Column(String(255))
    contact_addr4 = Column(String(255))
    telephone = Column(String(255))
    paid_thru_date = Column(DateTime(True))
    payment_info = Column(String(255))
    note1 = Column(String(255))
    note2 = Column(String(255))


class FirmPropertyMyuser(Base):
    __tablename__ = 'firm_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(5))
    category_code = Column(String(1))
    contact_name = Column(String(255))
    contact_addr1 = Column(String(255))
    contact_addr2 = Column(String(255))
    contact_addr3 = Column(String(255))
    contact_addr4 = Column(String(255))
    telephone = Column(String(255))
    paid_thru_date = Column(DateTime(True))
    payment_info = Column(String(255))
    note1 = Column(String(255))
    note2 = Column(String(255))
    name = Column(String(255))


class FirmPropertyName(Base):
    __tablename__ = 'firm_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    firm_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class FixfldType(Base):
    __tablename__ = 'fixfld_type'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)
    record_type_code = Column(CHAR(1))
    is_enabled = Column(Boolean)


class FixfldTypeMyuser(Base):
    __tablename__ = 'fixfld_type_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    name = Column(String(255))


class FixfldTypeName(Base):
    __tablename__ = 'fixfld_type_name'
    __table_args__ = {'schema': 'sierra_view'}

    fixfld_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class ForeignCurrency(Base):
    __tablename__ = 'foreign_currency'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    accounting_code_num = Column(Integer)
    code = Column(String(5))
    rate = Column(Numeric(30, 6))
    description = Column(String(256))
    format = Column(String(10))


class FormProperty(Base):
    __tablename__ = 'form_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)


class FormPropertyMyuser(Base):
    __tablename__ = 'form_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    name = Column(String(255))


class FormPropertyName(Base):
    __tablename__ = 'form_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    form_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class Function(Base):
    __tablename__ = 'function'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    display_order = Column(Integer)
    code = Column(String(255))
    function_category_id = Column(Integer)


class FunctionCategory(Base):
    __tablename__ = 'function_category'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    display_order = Column(Integer)
    code = Column(String(255))


class Fund(Base):
    __tablename__ = 'fund'
    __table_args__ = {'schema': 'sierra_view'}

    acct_unit = Column(Integer)
    fund_type = Column(String(255))
    fund_code = Column(String(255))
    external_fund = Column(Integer)
    appropriation = Column(Integer)
    expenditure = Column(Integer)
    encumbrance = Column(Integer)
    num_orders = Column(Integer)
    num_payments = Column(Integer)
    warning_percent = Column(Integer)
    discount_percent = Column(Integer)





class FundMyuser(Base):
    __tablename__ = 'fund_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    acct_unit = Column(Integer)
    fund_type = Column(String(255))
    fund_master_id = Column(Integer)
    fund_code = Column(String(255))
    external_fund_code_num = Column(Integer)
    appropriation = Column(Integer)
    expenditure = Column(Integer)
    encumbrance = Column(Integer)
    num_orders = Column(Integer)
    num_payments = Column(Integer)
    warning_percent = Column(Integer)
    discount_percent = Column(Integer)
    name = Column(String(255))
    note1 = Column(String(255))
    note2 = Column(String(255))


class FundProperty(Base):
    __tablename__ = 'fund_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    fund_master_id = Column(Integer)
    fund_type_id = Column(Integer)
    external_fund_property_id = Column(Integer)
    warning_percent = Column(Integer)
    discount_percent = Column(Integer)
    user_code1 = Column(String(255))
    user_code2 = Column(String(255))
    user_code3 = Column(String(255))
    is_active = Column(Boolean)


class FundPropertyName(Base):
    __tablename__ = 'fund_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    fund_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))
    note1 = Column(String(255))
    note2 = Column(String(255))


class FundSummary(Base):
    __tablename__ = 'fund_summary'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    fund_property_id = Column(Integer)
    appropriation = Column(Integer)
    expenditure = Column(Integer)
    encumbrance = Column(Integer)
    num_orders = Column(Integer)
    num_payments = Column(Integer)


class FundSummarySubfund(Base):
    __tablename__ = 'fund_summary_subfund'
    __table_args__ = {'schema': 'sierra_view'}

    fund_summary_id = Column(Integer)
    code = Column(String(255))
    value = Column(Integer)


class FundType(Base):
    __tablename__ = 'fund_type'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(255))


class FundTypeSummary(Base):
    __tablename__ = 'fund_type_summary'
    __table_args__ = {'schema': 'sierra_view'}

    accounting_unit_id = Column(Integer)
    fund_type_id = Column(Integer)
    last_lien_num = Column(Integer)
    last_voucher_num = Column(Integer)


class GtypeProperty(Base):
    __tablename__ = 'gtype_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code_num = Column(Integer)
    display_order = Column(Integer)


class GtypePropertyMyuser(Base):
    __tablename__ = 'gtype_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class GtypePropertyName(Base):
    __tablename__ = 'gtype_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    gtype_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class Hold(Base):
    __tablename__ = 'hold'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    patron_record_id = Column(BigInteger)
    record_id = Column(BigInteger)
    placed_gmt = Column(DateTime(True))
    is_frozen = Column(Boolean)
    delay_days = Column(Integer)
    location_code = Column(String(5))
    expires_gmt = Column(DateTime(True))
    status = Column(CHAR(1))
    is_ir = Column(Boolean)
    pickup_location_code = Column(String(5))
    is_ill = Column(Boolean)
    note = Column(String(128))
    ir_pickup_location_code = Column(String(5))
    ir_print_name = Column(String(255))
    ir_delivery_stop_name = Column(String(255))
    is_ir_converted_request = Column(Boolean)
    patron_records_display_order = Column(Integer)
    records_display_order = Column(Integer)


class HoldingRecord(Base):
    __tablename__ = 'holding_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    is_inherit_loc = Column(Boolean)
    allocation_rule_code = Column(CHAR(1))
    accounting_unit_code_num = Column(Integer)
    label_code = Column(CHAR(1))
    scode1 = Column(CHAR(1))
    scode2 = Column(CHAR(1))
    claimon_date_gmt = Column(DateTime(True))
    receiving_location_code = Column(String(3))
    vendor_code = Column(String(5))
    scode3 = Column(CHAR(1))
    scode4 = Column(CHAR(1))
    update_cnt = Column(CHAR(1))
    piece_cnt = Column(Integer)
    echeckin_code = Column(CHAR(1))
    media_type_code = Column(CHAR(1))
    is_suppressed = Column(Boolean)


class HoldingRecordAddressType(Base):
    __tablename__ = 'holding_record_address_type'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    code = Column(CHAR(1))


class HoldingRecordBox(Base):
    __tablename__ = 'holding_record_box'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    holding_record_cardlink_id = Column(BigInteger)
    box_count = Column(Integer)
    enum_level_a = Column(String(256))
    enum_level_b = Column(String(256))
    enum_level_c = Column(String(256))
    enum_level_d = Column(String(256))
    enum_level_e = Column(String(256))
    enum_level_f = Column(String(256))
    enum_level_g = Column(String(256))
    enum_level_h = Column(String(256))
    chron_level_i = Column(String(256))
    chron_level_i_trans_date = Column(String(256))
    chron_level_j = Column(String(256))
    chron_level_j_trans_date = Column(String(256))
    chron_level_k = Column(String(256))
    chron_level_k_trans_date = Column(String(256))
    chron_level_l = Column(String(256))
    chron_level_l_trans_date = Column(String(256))
    chron_level_m = Column(String(256))
    chron_level_m_trans_date = Column(String(256))
    note = Column(String(256))
    box_status_code = Column(CHAR(1))
    claim_cnt = Column(Integer)
    copies_cnt = Column(Integer)
    url = Column(String(256))
    is_suppressed = Column(Boolean)
    staff_note = Column(String(256))


class HoldingRecordBoxItem(Base):
    __tablename__ = 'holding_record_box_item'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    holding_record_box_id = Column(BigInteger)
    item_record_metadata_id = Column(BigInteger)


class HoldingRecordCard(Base):
    __tablename__ = 'holding_record_card'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    holding_record_id = Column(BigInteger)
    status_code = Column(CHAR(1))
    display_format_code = Column(CHAR(1))
    is_suppress_opac_display = Column(Boolean)
    order_record_metadata_id = Column(BigInteger)
    is_create_item = Column(Boolean)
    is_usmarc = Column(Boolean)
    is_marc = Column(Boolean)
    is_use_default_enum = Column(Boolean)
    is_use_default_date = Column(Boolean)
    update_method_code = Column(CHAR(1))


class HoldingRecordCardlink(Base):
    __tablename__ = 'holding_record_cardlink'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    holding_record_card_id = Column(BigInteger)
    card_type_code = Column(CHAR(1))
    link_count = Column(Integer)
    enum_level_a = Column(String(256))
    enum_level_a_disp_mode = Column(CHAR(1))
    enum_level_b = Column(String(256))
    enum_level_b_limit = Column(Integer)
    enum_level_b_rollover = Column(CHAR(1))
    enum_level_b_disp_mode = Column(CHAR(1))
    enum_level_c = Column(String(256))
    enum_level_c_limit = Column(Integer)
    enum_level_c_rollover = Column(CHAR(1))
    enum_level_c_disp_mode = Column(CHAR(1))
    enum_level_d = Column(String(256))
    enum_level_d_limit = Column(Integer)
    enum_level_d_rollover = Column(CHAR(1))
    enum_level_d_disp_mode = Column(CHAR(1))
    enum_level_e = Column(String(256))
    enum_level_e_limit = Column(Integer)
    enum_level_e_rollover = Column(CHAR(1))
    enum_level_e_disp_mode = Column(CHAR(1))
    enum_level_f = Column(String(256))
    enum_level_f_limit = Column(Integer)
    enum_level_f_rollover = Column(CHAR(1))
    enum_level_f_disp_mode = Column(CHAR(1))
    alt_enum_level_g = Column(String(256))
    alt_enum_level_g_disp_mode = Column(CHAR(1))
    alt_enum_level_h = Column(String(256))
    alt_enum_level_h_disp_mode = Column(CHAR(1))
    chron_level_i = Column(String(256))
    chron_level_j = Column(String(256))
    chron_level_k = Column(String(256))
    chron_level_l = Column(String(256))
    chron_level_m = Column(String(256))
    frequency_code = Column(String(10))
    calendar_change = Column(String(256))
    opac_label = Column(String(256))
    is_advanced = Column(Boolean)
    days_btw_iss = Column(Integer)
    claim_days = Column(Integer)
    bind_unit = Column(Integer)
    bind_delay = Column(Integer)
    is_bind_with_issue = Column(Boolean)
    is_use_autumn = Column(Boolean)
    enum_level_count = Column(Integer)
    alt_enum_level_count = Column(Integer)
    current_item = Column(Integer)
    alt_enum_level_h_limit = Column(Integer)
    alt_enum_level_h_rollover = Column(CHAR(1))


class HoldingRecordErmHolding(Base):
    __tablename__ = 'holding_record_erm_holding'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    holding_record_id = Column(BigInteger)
    varfield_type_code = Column(CHAR(1))
    marc_tag = Column(String(3))
    marc_ind1 = Column(CHAR(1))
    marc_ind2 = Column(CHAR(1))
    occ_num = Column(Integer)
    field_content = Column(String(20001))


class HoldingRecordItemRecordLink(Base):
    __tablename__ = 'holding_record_item_record_link'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    holding_record_id = Column(BigInteger)
    item_record_id = Column(BigInteger)
    items_display_order = Column(Integer)
    holdings_display_order = Column(Integer)


class HoldingRecordLocation(Base):
    __tablename__ = 'holding_record_location'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    holding_record_id = Column(BigInteger)
    copies = Column(Integer)
    location_code = Column(String(5))
    display_order = Column(Integer)


class HoldingRecordRouting(Base):
    __tablename__ = 'holding_record_routing'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    holding_record_id = Column(BigInteger)
    copy_num = Column(Integer)
    display_order = Column(Integer)
    is_patron_routing = Column(Boolean)
    priority_num = Column(Integer)
    patron_record_metadata_id = Column(BigInteger)
    routefile_code_num = Column(Integer)
    iii_user_name = Column(String(3))
    field_position = Column(Integer)


class HoldingView(Base):
    __tablename__ = 'holding_view'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    is_inherit_loc = Column(Boolean)
    allocation_rule_code = Column(CHAR(1))
    accounting_unit_code_num = Column(Integer)
    label_code = Column(CHAR(1))
    scode1 = Column(CHAR(1))
    scode2 = Column(CHAR(1))
    update_cnt = Column(CHAR(1))
    piece_cnt = Column(Integer)
    echeckin_code = Column(CHAR(1))
    media_type_code = Column(CHAR(1))
    is_suppressed = Column(Boolean)
    record_creation_date_gmt = Column(DateTime(True))


class IiiLanguage(Base):
    __tablename__ = 'iii_language'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    description = Column(String(64))
    staff_enabled = Column(Boolean)
    public_enabled = Column(Boolean)
    display_order = Column(Integer)
    is_right_to_left = Column(Boolean)


class IiiLanguageMyuser(Base):
    __tablename__ = 'iii_language_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    description = Column(String(64))
    staff_enabled = Column(Boolean)
    public_enabled = Column(Boolean)
    display_order = Column(Integer)
    is_right_to_left = Column(Boolean)


class IiiLanguageName(Base):
    __tablename__ = 'iii_language_name'
    __table_args__ = {'schema': 'sierra_view'}

    iii_language_id = Column(Integer)
    description = Column(String(255))
    name_iii_language_id = Column(Integer)


class IiiRole(Base):
    __tablename__ = 'iii_role'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(255))
    iii_role_category_id = Column(Integer)
    is_disabled_during_read_only_access = Column(Boolean)


class IiiRoleCategory(Base):
    __tablename__ = 'iii_role_category'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(255))


class IiiRoleCategoryName(Base):
    __tablename__ = 'iii_role_category_name'
    __table_args__ = {'schema': 'sierra_view'}

    iii_language_id = Column(Integer)
    iii_role_category_id = Column(Integer)
    name = Column(String(255))


class IiiRoleName(Base):
    __tablename__ = 'iii_role_name'
    __table_args__ = {'schema': 'sierra_view'}

    iii_role_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class IiiUser(Base):
    __tablename__ = 'iii_user'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    name = Column(String(255))
    location_group_port_number = Column(Integer)
    iii_user_group_code = Column(String(255))
    full_name = Column(String(255))
    iii_language_id = Column(Integer)
    account_unit = Column(Integer)
    statistic_group_code_num = Column(Integer)
    system_option_group_code_num = Column(Integer)
    timeout_warning_seconds = Column(Integer)
    timeout_logout_seconds = Column(Integer)
    scope_menu_id = Column(Integer)
    scope_menu_bitmask = Column(String(2048))
    is_new_account = Column(Boolean)
    last_password_change_gmt = Column(DateTime(True))
    is_exempt = Column(Boolean)
    is_suspended = Column(Boolean)
    is_context_only = Column(Boolean)


class IiiUserApplicationMyuser(Base):
    __tablename__ = 'iii_user_application_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    iii_user_id = Column(Integer)
    user_name = Column(String(255))
    application_code = Column(String(255))
    application_name = Column(String(255))


class IiiUserDesktopOption(Base):
    __tablename__ = 'iii_user_desktop_option'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    iii_user_id = Column(Integer)
    desktop_option_id = Column(Integer)
    value = Column(String(5000))


class IiiUserFundMaster(Base):
    __tablename__ = 'iii_user_fund_master'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    iii_user_id = Column(Integer)
    fund_master_id = Column(Integer)


class IiiUserGroup(Base):
    __tablename__ = 'iii_user_group'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    code = Column(String(255))
    concurrent_max = Column(Integer)
    is_independent = Column(Boolean)


class IiiUserIiiRole(Base):
    __tablename__ = 'iii_user_iii_role'
    __table_args__ = {'schema': 'sierra_view'}

    iii_user_id = Column(Integer)
    iii_role_id = Column(Integer)


class IiiUserLocation(Base):
    __tablename__ = 'iii_user_location'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    iii_user_id = Column(Integer)
    location_code = Column(String(5))


class IiiUserPermissionMyuser(Base):
    __tablename__ = 'iii_user_permission_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    iii_user_id = Column(Integer)
    user_name = Column(String(255))
    permission_num = Column(Integer)
    permission_code = Column(String(255))
    permission_name = Column(String(255))


class IiiUserPrinterMyuser(Base):
    __tablename__ = 'iii_user_printer_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    iii_user_id = Column(Integer)
    user_name = Column(String(255))
    printer_code_num = Column(Integer)
    name = Column(String(255))


class IiiUserWorkflow(Base):
    __tablename__ = 'iii_user_workflow'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    iii_user_id = Column(Integer)
    workflow_id = Column(Integer)
    display_order = Column(Integer)


class IiiUserWorkflowMyuser(Base):
    __tablename__ = 'iii_user_workflow_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    iii_user_id = Column(Integer)
    user_name = Column(String(255))
    workflow_name = Column(String(255))
    workflow_menu_name = Column(String(255))
    display_order = Column(Integer)


class InvoiceRecord(Base):
    __tablename__ = 'invoice_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    accounting_unit_code_num = Column(Integer)
    invoice_date_gmt = Column(DateTime(True))
    paid_date_gmt = Column(DateTime(True))
    status_code = Column(String(20))
    posted_data_gmt = Column(DateTime(True))
    is_paid_date_received_date = Column(Boolean)
    ncode1 = Column(CHAR(1))
    ncode2 = Column(CHAR(1))
    ncode3 = Column(CHAR(1))
    invoice_number_text = Column(String(20))
    iii_user_name = Column(String(20))
    foreign_currency_code = Column(String(20))
    foreign_currency_format = Column(String(30))
    foreign_currency_exchange_rate = Column(Numeric(30, 6))
    tax_fund_code = Column(String(20))
    tax_type_code = Column(String(30))
    discount_amt = Column(Numeric(30, 6))
    grand_total_amt = Column(Numeric(30, 6))
    subtotal_amt = Column(Numeric(30, 6))
    shipping_amt = Column(Numeric(30, 6))
    total_tax_amt = Column(Numeric(30, 6))
    use_tax_fund_code = Column(String(20))
    use_tax_percentage_rate = Column(Numeric(30, 6))
    use_tax_type_code = Column(String(10))
    use_tax_ship_service_code = Column(String(10))
    is_suppressed = Column(Boolean)


class InvoiceRecordLine(Base):
    __tablename__ = 'invoice_record_line'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    invoice_record_id = Column(BigInteger)
    order_record_metadata_id = Column(BigInteger)
    paid_amt = Column(Numeric(30, 6))
    lien_amt = Column(Numeric(30, 6))
    lien_flag = Column(Integer)
    list_price = Column(Numeric(30, 6))
    fund_code = Column(String(20))
    subfund_num = Column(Integer)
    copies_paid_cnt = Column(Integer)
    external_fund_code_num = Column(Integer)
    status_code = Column(String(5))
    note = Column(String(20001))
    is_single_copy_partial_pmt = Column(Boolean)
    title = Column(String(20001))
    multiflag_code = Column(CHAR(1))
    line_level_tax = Column(Numeric(30, 6))
    vendor_code = Column(String(5))
    accounting_transaction_voucher_num = Column(Integer)
    accounting_transaction_voucher_seq_num = Column(Integer)
    line_cnt = Column(Integer)
    invoice_record_vendor_summary_id = Column(BigInteger)
    is_use_tax = Column(Boolean)


class InvoiceRecordVendorSummary(Base):
    __tablename__ = 'invoice_record_vendor_summary'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    invoice_record_id = Column(BigInteger)
    vendor_code = Column(String(5))
    vendor_address_line1 = Column(String(1000))
    voucher_num = Column(Integer)
    voucher_total = Column(Integer)
    display_order = Column(Integer)


class InvoiceView(Base):
    __tablename__ = 'invoice_view'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    accounting_unit_code_num = Column(Integer)
    invoice_date_gmt = Column(DateTime(True))
    paid_date_gmt = Column(DateTime(True))
    status_code = Column(String(20))
    posted_date_gmt = Column(DateTime(True))
    is_paid_date_received_date = Column(Boolean)
    ncode1 = Column(CHAR(1))
    ncode2 = Column(CHAR(1))
    ncode3 = Column(CHAR(1))
    invoice_number_text = Column(String(20))
    iii_user_name = Column(String(20))
    foreign_currency_code = Column(String(20))
    foreign_currency_format = Column(String(30))
    foreign_currency_exchange_rate = Column(Numeric(30, 6))
    tax_fund_code = Column(String(20))
    tax_type_code = Column(String(30))
    discount_amt = Column(Numeric(30, 6))
    grand_total_amt = Column(Numeric(30, 6))
    subtotal_amt = Column(Numeric(30, 6))
    shipping_amt = Column(Numeric(30, 6))
    total_tax_amt = Column(Numeric(30, 6))
    use_tax_fund_code = Column(String(20))
    use_tax_percentage_rate = Column(Numeric(30, 6))
    use_tax_type_code = Column(String(10))
    use_tax_ship_service_code = Column(String(10))
    is_suppressed = Column(Boolean)
    record_creation_date_gmt = Column(DateTime(True))


class ItemCircHistory(Base):
    __tablename__ = 'item_circ_history'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    item_record_metadata_id = Column(BigInteger)
    patron_record_metadata_id = Column(BigInteger)
    checkout_gmt = Column(DateTime(True))
    checkin_gmt = Column(DateTime(True))


class ItemRecord(Base):
    __tablename__ = 'item_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    icode1 = Column(Integer)
    icode2 = Column(CHAR(1))
    itype_code_num = Column(SmallInteger)
    location_code = Column(String(5))
    agency_code_num = Column(SmallInteger)
    item_status_code = Column(String(3))
    is_inherit_loc = Column(Boolean)
    price = Column(Numeric(30, 6))
    last_checkin_gmt = Column(DateTime(True))
    checkout_total = Column(Integer)
    renewal_total = Column(Integer)
    last_year_to_date_checkout_total = Column(Integer)
    year_to_date_checkout_total = Column(Integer)
    is_bib_hold = Column(Boolean)
    copy_num = Column(Integer)
    checkout_statistic_group_code_num = Column(Integer)
    last_patron_record_metadata_id = Column(BigInteger)
    inventory_gmt = Column(DateTime(True))
    checkin_statistics_group_code_num = Column(Integer)
    use3_count = Column(Integer)
    last_checkout_gmt = Column(DateTime(True))
    internal_use_count = Column(Integer)
    copy_use_count = Column(Integer)
    item_message_code = Column(CHAR(1))
    opac_message_code = Column(CHAR(1))
    virtual_type_code = Column(CHAR(1))
    virtual_item_central_code_num = Column(Integer)
    holdings_code = Column(CHAR(1))
    save_itype_code_num = Column(SmallInteger)
    save_location_code = Column(String(5))
    save_checkout_total = Column(Integer)
    old_location_code = Column(String(5))
    distance_learning_status = Column(SmallInteger)
    is_suppressed = Column(Boolean)
    is_available_at_library = Column(Boolean)


class ItemRecordProperty(Base):
    __tablename__ = 'item_record_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    item_record_id = Column(BigInteger)
    call_number = Column(String(1000))
    call_number_norm = Column(String(1000))
    barcode = Column(String(1000))


class ItemStatusProperty(Base):
    __tablename__ = 'item_status_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    code = Column(String(3))
    display_order = Column(Integer)


class ItemStatusPropertyMyuser(Base):
    __tablename__ = 'item_status_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    name = Column(String(255))


class ItemStatusPropertyName(Base):
    __tablename__ = 'item_status_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    item_status_property_id = Column(BigInteger)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class ItemView(Base):
    __tablename__ = 'item_view'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    barcode = Column(String(1000))
    icode1 = Column(Integer)
    icode2 = Column(CHAR(1))
    itype_code_num = Column(SmallInteger)
    location_code = Column(String(5))
    agency_code_num = Column(SmallInteger)
    item_status_code = Column(String(3))
    is_inherit_loc = Column(Boolean)
    price = Column(Numeric(30, 6))
    last_checkin_gmt = Column(DateTime(True))
    checkout_total = Column(Integer)
    renewal_total = Column(Integer)
    last_year_to_date_checkout_total = Column(Integer)
    year_to_date_checkout_total = Column(Integer)
    is_bib_hold = Column(Boolean)
    copy_num = Column(Integer)
    checkout_statistic_group_code_num = Column(Integer)
    last_patron_record_metadata_id = Column(BigInteger)
    inventory_gmt = Column(DateTime(True))
    checkin_statistics_group_code_num = Column(Integer)
    use3_count = Column(Integer)
    last_checkout_gmt = Column(DateTime(True))
    internal_use_count = Column(Integer)
    copy_use_count = Column(Integer)
    item_message_code = Column(CHAR(1))
    opac_message_code = Column(CHAR(1))
    virtual_type_code = Column(CHAR(1))
    virtual_item_central_code_num = Column(Integer)
    holdings_code = Column(CHAR(1))
    save_itype_code_num = Column(SmallInteger)
    save_location_code = Column(String(5))
    save_checkout_total = Column(Integer)
    old_location_code = Column(String(5))
    distance_learning_status = Column(SmallInteger)
    is_suppressed = Column(Boolean)
    record_creation_date_gmt = Column(DateTime(True))


class ItypeProperty(Base):
    __tablename__ = 'itype_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code_num = Column(Integer)
    display_order = Column(Integer)
    itype_property_category_id = Column(Integer)
    physical_format_id = Column(Integer)
    target_audience_id = Column(Integer)
    collection_id = Column(Integer)


class ItypePropertyCategory(Base):
    __tablename__ = 'itype_property_category'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    display_order = Column(Integer)
    is_default = Column(Boolean)


class ItypePropertyCategoryMyuser(Base):
    __tablename__ = 'itype_property_category_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(Integer)
    display_order = Column(Integer)
    itype_property_category_id = Column(Integer)
    physical_format_id = Column(Integer)
    target_audience_id = Column(Integer)
    name = Column(String(255))


class ItypePropertyCategoryName(Base):
    __tablename__ = 'itype_property_category_name'
    __table_args__ = {'schema': 'sierra_view'}

    itype_property_category_id = Column(Integer)
    name = Column(String(255))
    iii_language_id = Column(Integer)


class ItypePropertyMyuser(Base):
    __tablename__ = 'itype_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(Integer)
    display_order = Column(Integer)
    itype_property_category_id = Column(Integer)
    physical_format_id = Column(Integer)
    target_audience_id = Column(Integer)
    name = Column(String(255))


class ItypePropertyName(Base):
    __tablename__ = 'itype_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    itype_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class KeywordSynonym(Base):
    __tablename__ = 'keyword_synonym'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    keyword = Column(String(255))
    synonym = Column(String(255))


class LanguageProperty(Base):
    __tablename__ = 'language_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)
    is_public = Column(Boolean)


class LanguagePropertyMyuser(Base):
    __tablename__ = 'language_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    is_public = Column(Boolean)
    name = Column(String(255))


class LanguagePropertyName(Base):
    __tablename__ = 'language_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    language_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class LeaderField(Base):
    __tablename__ = 'leader_field'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    record_status_code = Column(CHAR(1))
    record_type_code = Column(CHAR(1))
    bib_level_code = Column(CHAR(1))
    control_type_code = Column(CHAR(1))
    char_encoding_scheme_code = Column(CHAR(1))
    encoding_level_code = Column(CHAR(1))
    descriptive_cat_form_code = Column(CHAR(1))
    multipart_level_code = Column(CHAR(1))
    base_address = Column(Integer)


class LicenseRecord(Base):
    __tablename__ = 'license_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    accounting_unit_code_num = Column(Integer)
    confidential_code = Column(CHAR(1))
    auto_renew_code = Column(CHAR(1))
    status_code = Column(CHAR(1))
    type_code = Column(CHAR(1))
    change_to_code = Column(CHAR(1))
    breach_procedure_code = Column(CHAR(1))
    termination_procedure_code = Column(CHAR(1))
    perpetual_access_code = Column(CHAR(1))
    archival_provisions_code = Column(CHAR(1))
    warranty_code = Column(CHAR(1))
    disability_compliance_code = Column(CHAR(1))
    performance_requirement_code = Column(CHAR(1))
    liability_code = Column(CHAR(1))
    idemnification_code = Column(CHAR(1))
    law_and_venue_code = Column(CHAR(1))
    user_confidentiality_code = Column(CHAR(1))
    suppress_code = Column(CHAR(1))
    lcode1 = Column(CHAR(1))
    lcode2 = Column(CHAR(1))
    lcode3 = Column(CHAR(1))
    concurrent_users_count = Column(Integer)
    license_sign_gmt = Column(DateTime(True))
    licensor_sign_gmt = Column(DateTime(True))
    contract_start_gmt = Column(DateTime(True))
    contract_end_gmt = Column(DateTime(True))
    breach_cure = Column(Integer)
    cancellation_notice = Column(Integer)
    is_suppressed = Column(Boolean)
    ldate4 = Column(DateTime(True))
    language_code = Column(String(3))
    country_code = Column(String(3))
    llang2 = Column(String(3))


class LicenseView(Base):
    __tablename__ = 'license_view'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    accounting_unit_code_num = Column(Integer)
    confidential_code = Column(CHAR(1))
    auto_renew_code = Column(CHAR(1))
    status_code = Column(CHAR(1))
    type_code = Column(CHAR(1))
    change_to_code = Column(CHAR(1))
    breach_procedure_code = Column(CHAR(1))
    termination_procedure_code = Column(CHAR(1))
    perpetual_access_code = Column(CHAR(1))
    archival_provisions_code = Column(CHAR(1))
    warranty_code = Column(CHAR(1))
    disability_compliance_code = Column(CHAR(1))
    performance_requirement_code = Column(CHAR(1))
    liability_code = Column(CHAR(1))
    idemnification_code = Column(CHAR(1))
    law_and_venue_code = Column(CHAR(1))
    user_confidentiality_code = Column(CHAR(1))
    suppress_code = Column(CHAR(1))
    lcode1 = Column(CHAR(1))
    lcode2 = Column(CHAR(1))
    lcode3 = Column(CHAR(1))
    concurrent_users_count = Column(Integer)
    license_sign_gmt = Column(DateTime(True))
    licensor_sign_gmt = Column(DateTime(True))
    contract_start_gmt = Column(DateTime(True))
    contract_end_gmt = Column(DateTime(True))
    breach_cure = Column(Integer)
    cancellation_notice = Column(Integer)
    record_creation_date_gmt = Column(DateTime(True))


class Location(Base):
    __tablename__ = 'location'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(5))
    branch_code_num = Column(Integer)
    parent_location_code = Column(String(5))
    is_public = Column(Boolean)
    is_requestable = Column(Boolean)


class LocationChange(Base):
    __tablename__ = 'location_change'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    location_code = Column(String(10))
    description = Column(String(1000))


class LocationMyuser(Base):
    __tablename__ = 'location_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(5))
    branch_code_num = Column(Integer)
    parent_location_code = Column(String(5))
    is_public = Column(Boolean)
    name = Column(String(255))


class LocationName(Base):
    __tablename__ = 'location_name'
    __table_args__ = {'schema': 'sierra_view'}

    location_id = Column(Integer)
    name = Column(String(255))
    iii_language_id = Column(Integer)


class LocationPropertyType(Base):
    __tablename__ = 'location_property_type'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(255))
    display_order = Column(Integer)
    default_value = Column(String(1024))
    is_single_value = Column(Boolean)
    is_enabled = Column(Boolean)


class LocationPropertyTypeMyuser(Base):
    __tablename__ = 'location_property_type_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    display_order = Column(Integer)
    default_value = Column(String(1024))
    is_single_value = Column(Boolean)
    is_enabled = Column(Boolean)
    name = Column(String(255))


class LocationPropertyTypeName(Base):
    __tablename__ = 'location_property_type_name'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    location_property_type_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class LocationPropertyValue(Base):
    __tablename__ = 'location_property_value'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    location_property_type_id = Column(Integer)
    location_id = Column(Integer)
    value = Column(String(1024))


class M2bmapCategory(Base):
    __tablename__ = 'm2bmap_category'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    name = Column(String(255))
    original_delimiter = Column(CHAR(1))
    is_case_sensitive = Column(Boolean)
    is_bar_subfield = Column(Boolean)
    is_chinese = Column(Boolean)
    is_stop_on_map = Column(Boolean)


class M2bmapEntry(Base):
    __tablename__ = 'm2bmap_entry'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    m2bmap_category_id = Column(Integer)
    display_order = Column(Integer)
    comparison = Column(String(200))
    replacement = Column(String(200))


class MarcExportFormat(Base):
    __tablename__ = 'marc_export_format'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    code = Column(String(20))
    code_name = Column(String(20))
    is_staff_enabled = Column(Boolean)


class MarcPreference(Base):
    __tablename__ = 'marc_preference'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    iii_user_name = Column(String(255))
    diacritic_category_id = Column(Integer)
    marc_export_format_id = Column(BigInteger)
    b2m_category_code = Column(String(20))
    is_default_preference = Column(Boolean)


class MarclabelType(Base):
    __tablename__ = 'marclabel_type'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    varfield_type_code = Column(String(1))
    marc_tag_pattern = Column(String(50))
    display_order = Column(Integer)


class MarclabelTypeMyuser(Base):
    __tablename__ = 'marclabel_type_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    record_type_code = Column(CHAR(1))
    varfield_type_code = Column(String(1))
    marctag_pattern = Column(String(50))
    display_order = Column(Integer)
    name = Column(String(255))


class MarclabelTypeName(Base):
    __tablename__ = 'marclabel_type_name'
    __table_args__ = {'schema': 'sierra_view'}

    marclabel_type_id = Column(BigInteger)
    iii_language_id = Column(BigInteger)
    name = Column(String(255))


class MaterialProperty(Base):
    __tablename__ = 'material_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)
    is_public = Column(Boolean)
    material_property_category_id = Column(Integer)
    physical_format_id = Column(Integer)


class MaterialPropertyCategory(Base):
    __tablename__ = 'material_property_category'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    display_order = Column(Integer)
    is_default = Column(Boolean)


class MaterialPropertyCategoryMyuser(Base):
    __tablename__ = 'material_property_category_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    is_default = Column(Boolean)
    name = Column(String(255))


class MaterialPropertyCategoryName(Base):
    __tablename__ = 'material_property_category_name'
    __table_args__ = {'schema': 'sierra_view'}

    material_property_category_id = Column(Integer)
    name = Column(String(255))
    iii_language_id = Column(Integer)


class MaterialPropertyMyuser(Base):
    __tablename__ = 'material_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    is_public = Column(Boolean)
    material_property_category_id = Column(Integer)
    physical_format_id = Column(Integer)
    name = Column(String(255))


class MaterialPropertyName(Base):
    __tablename__ = 'material_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    material_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))
    facet_text = Column(String(500))


class MblockProperty(Base):
    __tablename__ = 'mblock_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)


class MblockPropertyMyuser(Base):
    __tablename__ = 'mblock_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    name = Column(String(255))


class MblockPropertyName(Base):
    __tablename__ = 'mblock_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    mblock_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class NetworkAccessView(Base):
    __tablename__ = 'network_access_view'
    __table_args__ = {'schema': 'sierra_view'}

    port = Column(Integer)
    is_enabled = Column(Boolean)
    is_super_user = Column(Boolean)
    ip_range = Column(String(255))
    is_accessible = Column(Boolean)
    login_name = Column(String(128))
    service_level = Column(Integer)
    comment = Column(String(255))


class NotificationMediumProperty(Base):
    __tablename__ = 'notification_medium_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)


class NotificationMediumPropertyMyuser(Base):
    __tablename__ = 'notification_medium_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    name = Column(String(255))


class NotificationMediumPropertyName(Base):
    __tablename__ = 'notification_medium_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    notification_medium_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class OaiCrosswalk(Base):
    __tablename__ = 'oai_crosswalk'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    marc_type = Column(CHAR(1))
    metadata_prefix = Column(String(32))
    name = Column(String(32))
    description = Column(String(255))
    is_system = Column(Boolean)


class OaiCrosswalkField(Base):
    __tablename__ = 'oai_crosswalk_field'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    oai_crosswalk_id = Column(BigInteger)
    element_name = Column(String(100))
    varfield_type_code = Column(CHAR(1))
    marc_tag = Column(CHAR(3))
    subfields = Column(String(26))
    is_add_subfield = Column(Boolean)
    is_varfield = Column(Boolean)
    fixnum = Column(Integer)
    order_num = Column(Integer)


class OrderNoteProperty(Base):
    __tablename__ = 'order_note_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)


class OrderNotePropertyMyuser(Base):
    __tablename__ = 'order_note_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    name = Column(String(255))


class OrderNotePropertyName(Base):
    __tablename__ = 'order_note_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    order_note_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))





class OrderRecordAddressType(Base):
    __tablename__ = 'order_record_address_type'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    code = Column(CHAR(1))





class OrderRecordEdifactResponse(Base):
    __tablename__ = 'order_record_edifact_response'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    order_record_id = Column(BigInteger)
    code = Column(String(20))
    message = Column(String(512))
    event_date_gmt = Column(DateTime(True))





class OrderRecordReceived(Base):
    __tablename__ = 'order_record_received'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    order_record_id = Column(BigInteger)
    location_code = Column(String(5))
    fund_code = Column(String(20))
    copy_num = Column(Integer)
    volume_num = Column(Integer)
    item_record_metadata_id = Column(BigInteger)
    received_date_gmt = Column(DateTime(True))
    display_order = Column(Integer)


class OrderStatusProperty(Base):
    __tablename__ = 'order_status_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)


class OrderStatusPropertyMyuser(Base):
    __tablename__ = 'order_status_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    name = Column(String(255))


class OrderStatusPropertyName(Base):
    __tablename__ = 'order_status_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    order_status_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class OrderTypeProperty(Base):
    __tablename__ = 'order_type_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)


class OrderTypePropertyMyuser(Base):
    __tablename__ = 'order_type_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    name = Column(String(255))


class OrderTypePropertyName(Base):
    __tablename__ = 'order_type_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    order_type_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))




class PatronRecord(Base):
    __tablename__ = 'patron_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    ptype_code = Column(SmallInteger)
    home_library_code = Column(String(5))
    expiration_date_gmt = Column(DateTime(True))
    pcode1 = Column(CHAR(1))
    pcode2 = Column(CHAR(1))
    pcode3 = Column(SmallInteger)
    pcode4 = Column(Integer)
    birth_date_gmt = Column(Date)
    mblock_code = Column(CHAR(1))
    firm_code = Column(String(5))
    block_until_date_gmt = Column(DateTime(True))
    patron_agency_code_num = Column(SmallInteger)
    iii_language_pref_code = Column(String(3))
    checkout_total = Column(Integer)
    renewal_total = Column(Integer)
    checkout_count = Column(Integer)
    patron_message_code = Column(CHAR(1))
    highest_level_overdue_num = Column(Integer)
    claims_returned_total = Column(Integer)
    owed_amt = Column(Numeric(30, 6))
    itema_count = Column(Integer)
    itemb_count = Column(Integer)
    overdue_penalty_count = Column(Integer)
    ill_checkout_total = Column(Integer)
    debit_amt = Column(Numeric(30, 6))
    itemc_count = Column(Integer)
    itemd_count = Column(Integer)
    activity_gmt = Column(DateTime(True))
    notification_medium_code = Column(CHAR(1))
    registration_count = Column(Integer)
    registration_total = Column(Integer)
    attendance_total = Column(Integer)
    waitlist_count = Column(Integer)
    is_reading_history_opt_in = Column(Boolean)


class PatronRecordAddres(Base):
    __tablename__ = 'patron_record_address'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    patron_record_id = Column(BigInteger)
    patron_record_address_type_id = Column(BigInteger)
    display_order = Column(Integer)
    addr1 = Column(String(1000))
    addr2 = Column(String(1000))
    addr3 = Column(String(1000))
    village = Column(String(1000))
    city = Column(String(1000))
    region = Column(String(1000))
    postal_code = Column(String(100))
    country = Column(String(1000))


class PatronRecordAddressType(Base):
    __tablename__ = 'patron_record_address_type'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    code = Column(CHAR(1))


class PatronRecordFullname(Base):
    __tablename__ = 'patron_record_fullname'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    patron_record_id = Column(BigInteger)
    display_order = Column(Integer)
    prefix = Column(String(50))
    first_name = Column(String(500))
    middle_name = Column(String(500))
    last_name = Column(String(500))
    suffix = Column(String(50))


class PatronRecordPhone(Base):
    __tablename__ = 'patron_record_phone'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    patron_record_id = Column(BigInteger)
    patron_record_phone_type_id = Column(BigInteger)
    display_order = Column(Integer)
    phone_number = Column(String(200))


class PatronRecordPhoneType(Base):
    __tablename__ = 'patron_record_phone_type'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    code = Column(CHAR(1))


class PatronView(Base):
    __tablename__ = 'patron_view'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    barcode = Column(String(512))
    ptype_code = Column(SmallInteger)
    home_library_code = Column(String(5))
    expiration_date_gmt = Column(DateTime(True))
    pcode1 = Column(CHAR(1))
    pcode2 = Column(CHAR(1))
    pcode3 = Column(SmallInteger)
    pcode4 = Column(Integer)
    birth_date_gmt = Column(Date)
    mblock_code = Column(CHAR(1))
    firm_code = Column(String(5))
    block_until_date_gmt = Column(DateTime(True))
    patron_agency_code_num = Column(SmallInteger)
    iii_language_pref_code = Column(String(3))
    checkout_total = Column(Integer)
    renewal_total = Column(Integer)
    checkout_count = Column(Integer)
    patron_message_code = Column(CHAR(1))
    highest_level_overdue_num = Column(Integer)
    claims_returned_total = Column(Integer)
    owed_amt = Column(Numeric(30, 6))
    itema_count = Column(Integer)
    itemb_count = Column(Integer)
    overdue_penalty_count = Column(Integer)
    ill_checkout_total = Column(Integer)
    debit_amt = Column(Numeric(30, 6))
    itemc_count = Column(Integer)
    itemd_count = Column(Integer)
    activity_gmt = Column(DateTime(True))
    notification_medium_code = Column(CHAR(1))
    registration_count = Column(Integer)
    registration_total = Column(Integer)
    attendance_total = Column(Integer)
    waitlist_count = Column(Integer)
    is_reading_history_opt_in = Column(Boolean)


class PatronsToExclude(Base):
    __tablename__ = 'patrons_to_exclude'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    patron_record_metadata_id = Column(BigInteger)
    time_added_to_table_gmt = Column(DateTime(True))


class Payment(Base):
    __tablename__ = 'payment'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    pmt_date_gmt = Column(DateTime)
    amt_paid = Column(Numeric(30, 6))
    pmt_type_code = Column(String(20))
    pmt_note = Column(String(255))
    patron_record_metadata_id = Column(BigInteger)


class Pblock(Base):
    __tablename__ = 'pblock'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    ptype_code_num = Column(Integer)
    ptype_agency_code_num = Column(Integer)
    is_expiration_date_active = Column(Boolean)
    max_owed_amt = Column(Numeric(30, 6))
    max_overdue_num = Column(Integer)
    max_item_num = Column(Integer)
    max_hold_num = Column(Integer)
    max_ill_item_num = Column(Integer)
    max_ill_item_per_period_num = Column(Integer)
    max_itema_num = Column(Integer)
    max_itemb_num = Column(Integer)
    max_itemc_num = Column(Integer)
    max_itemd_num = Column(Integer)
    max_registration_num = Column(Integer)
    max_penalty_point_num = Column(Integer)
    penalty_point_days = Column(Integer)


class PhraseEntry(Base):
    __tablename__ = 'phrase_entry'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    index_tag = Column(String(20))
    varfield_type_code = Column(String(20))
    occurrence = Column(Integer)
    is_permuted = Column(Boolean)
    type2 = Column(Integer)
    type3 = Column(CHAR(1))
    index_entry = Column(String(512))
    insert_title = Column(String(256))
    phrase_rule_rule_num = Column(Integer)
    phrase_rule_operation = Column(String(1))
    phrase_rule_subfield_list = Column(String(50))
    original_content = Column(String(1000))
    parent_record_id = Column(BigInteger)
    insert_title_tag = Column(String(1))
    insert_title_occ = Column(Integer)


class PhraseRule(Base):
    __tablename__ = 'phrase_rule'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    varfield_type_code = Column(String(1))
    marc_tag_pattern = Column(String(50))
    operation = Column(String(1))
    subfield_list = Column(String(50))
    phrase_type_code = Column(String(1))
    rule_num = Column(Integer)
    is_continue = Column(Boolean)
    display_order = Column(Integer)


class PhraseType(Base):
    __tablename__ = 'phrase_type'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    varfield_type_code = Column(CHAR(1))
    display_order = Column(Integer)


class PhraseTypeName(Base):
    __tablename__ = 'phrase_type_name'
    __table_args__ = {'schema': 'sierra_view'}

    phrase_type_id = Column(BigInteger)
    iii_language_id = Column(BigInteger)
    name = Column(String(255))
    plural_name = Column(String(255))


class PhysicalFormat(Base):
    __tablename__ = 'physical_format'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    is_default = Column(Boolean)
    display_order = Column(Integer)


class PhysicalFormatMyuser(Base):
    __tablename__ = 'physical_format_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    is_default = Column(Boolean)
    display_order = Column(Integer)
    name = Column(String(255))


class PhysicalFormatName(Base):
    __tablename__ = 'physical_format_name'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    name = Column(String(255))
    iii_language_id = Column(Integer)
    physical_format_id = Column(Integer)


class ProgramRecord(Base):
    __tablename__ = 'program_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    program_name = Column(String(1024))
    reg_allowed_code = Column(CHAR(1))
    allocation_rule_code = Column(CHAR(1))
    cost = Column(Numeric(30, 6))
    eligibility_code = Column(CHAR(1))
    publication_start_date_gmt = Column(DateTime)
    publication_end_date_gmt = Column(DateTime)
    tickler_days_to_start = Column(Integer)
    min_alert_days_to_start = Column(Integer)
    max_alert_seats_open = Column(Integer)
    reg_per_patron = Column(Integer)
    program_type_code = Column(Integer)
    auto_transfer_code = Column(CHAR(1))
    is_right_result_exact = Column(Boolean)
    gcode1 = Column(CHAR(1))
    gcode2 = Column(CHAR(1))
    gcode3 = Column(CHAR(1))
    is_suppressed = Column(Boolean)


class ProgramRecordLocation(Base):
    __tablename__ = 'program_record_location'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    program_record_id = Column(BigInteger)
    location_code = Column(String(5))
    display_order = Column(Integer)


class ProgramView(Base):
    __tablename__ = 'program_view'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    program_name = Column(String(1024))
    reg_allowed_code = Column(CHAR(1))
    allocation_rule_code = Column(CHAR(1))
    cost = Column(Numeric(30, 6))
    eligibility_code = Column(CHAR(1))
    publication_start_date_gmt = Column(DateTime)
    publication_end_date_gmt = Column(DateTime)
    tickler_days_to_start = Column(Integer)
    min_alert_days_to_start = Column(Integer)
    max_alert_seats_open = Column(Integer)
    reg_per_patron = Column(Integer)
    program_type_code = Column(Integer)
    auto_transfer_code = Column(CHAR(1))
    is_right_result_exact = Column(Boolean)
    gcode1 = Column(CHAR(1))
    gcode2 = Column(CHAR(1))
    gcode3 = Column(CHAR(1))
    is_suppressed = Column(Boolean)
    record_creation_date_gmt = Column(DateTime(True))


class PtypeProperty(Base):
    __tablename__ = 'ptype_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    value = Column(SmallInteger)
    tagging_allowed = Column(Boolean)
    display_order = Column(Integer)
    is_force_right_result_exact_allowed = Column(Boolean)
    is_comment_auto_approved = Column(Boolean)
    ptype_category_id = Column(Integer)


class PtypePropertyCategory(Base):
    __tablename__ = 'ptype_property_category'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    display_order = Column(Integer)
    is_default = Column(Boolean)


class PtypePropertyCategoryMyuser(Base):
    __tablename__ = 'ptype_property_category_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    display_order = Column(Integer)
    is_default = Column(Boolean)
    name = Column(String(255))


class PtypePropertyCategoryName(Base):
    __tablename__ = 'ptype_property_category_name'
    __table_args__ = {'schema': 'sierra_view'}

    ptype_category_id = Column(Integer)
    name = Column(String(255))
    iii_language_id = Column(Integer)


class PtypePropertyMyuser(Base):
    __tablename__ = 'ptype_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    value = Column(SmallInteger)
    tagging_allowed = Column(Boolean)
    display_order = Column(Integer)
    is_force_right_result_exact_allowed = Column(Boolean)
    is_comment_auto_approved = Column(Boolean)
    ptype_category_id = Column(Integer)
    name = Column(String(255))


class PtypePropertyName(Base):
    __tablename__ = 'ptype_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    ptype_id = Column(Integer)
    description = Column(String(255))
    iii_language_id = Column(Integer)


class ReadingHistory(Base):
    __tablename__ = 'reading_history'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    bib_record_metadata_id = Column(BigInteger)
    item_record_metadata_id = Column(BigInteger)
    patron_record_metadata_id = Column(BigInteger)
    checkout_gmt = Column(DateTime(True))


class ReceivingActionProperty(Base):
    __tablename__ = 'receiving_action_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)


class ReceivingActionPropertyMyuser(Base):
    __tablename__ = 'receiving_action_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    name = Column(String(255))


class ReceivingActionPropertyName(Base):
    __tablename__ = 'receiving_action_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    receiving_action_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class ReceivingLocationProperty(Base):
    __tablename__ = 'receiving_location_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(CHAR(1))
    display_order = Column(Integer)


class ReceivingLocationPropertyMyuser(Base):
    __tablename__ = 'receiving_location_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(CHAR(1))
    display_order = Column(Integer)
    name = Column(String(255))


class ReceivingLocationPropertyName(Base):
    __tablename__ = 'receiving_location_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    receiving_location_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class RecordLock(Base):
    __tablename__ = 'record_lock'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)





class RecordRange(Base):
    __tablename__ = 'record_range'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    accounting_unit_code_num = Column(Integer)
    start_num = Column(Integer)
    last = Column(BigInteger)
    current_count = Column(Integer)
    deleted_count = Column(Integer)
    max_num = Column(Integer)
    size = Column(Integer)


class RecordType(Base):
    __tablename__ = 'record_type'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(CHAR(1))
    tag = Column(CHAR(1))


class RecordTypeMyuser(Base):
    __tablename__ = 'record_type_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(CHAR(1))
    tag = Column(CHAR(1))
    name = Column(String(255))


class RecordTypeName(Base):
    __tablename__ = 'record_type_name'
    __table_args__ = {'schema': 'sierra_view'}

    record_type_id = Column(Integer)
    name = Column(String(255))
    iii_language_id = Column(Integer)


class Request(Base):
    __tablename__ = 'request'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    patron_record_id = Column(BigInteger)
    item_record_id = Column(BigInteger)
    items_display_order = Column(Integer)
    ptype = Column(SmallInteger)
    patrons_display_order = Column(Integer)
    request_gmt = Column(DateTime(True))
    pickup_anywhere_location_code = Column(String(5))
    central_location_code = Column(String(5))
    transaction_num = Column(Integer)
    remote_patron_record_key = Column(String(100))
    dl_pickup_location_code_num = Column(Integer)


class RequestRule(Base):
    __tablename__ = 'request_rule'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    query = Column(Text)
    sql_query = Column(Text)


class RequestRuleComment(Base):
    __tablename__ = 'request_rule_comment'
    __table_args__ = {'schema': 'sierra_view'}

    request_rule_id = Column(Integer)
    comment = Column(Text)
    iii_language_id = Column(Integer)
    id = Column(Integer)


class ResourceRecord(Base):
    __tablename__ = 'resource_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    is_right_result_exact = Column(Boolean)
    rights_code = Column(CHAR(1))
    suppress_code = Column(CHAR(1))
    ecode1 = Column(CHAR(1))
    ecode2 = Column(CHAR(1))
    ecode3 = Column(CHAR(1))
    ecode4 = Column(CHAR(1))
    resource_status_code = Column(CHAR(1))
    package_code = Column(CHAR(1))
    trial_begin_gmt = Column(DateTime(True))
    trial_end_gmt = Column(DateTime(True))
    renewal_gmt = Column(DateTime(True))
    registration_gmt = Column(DateTime(True))
    activation_gmt = Column(DateTime(True))
    edate5_gmt = Column(DateTime(True))
    edate6_gmt = Column(DateTime(True))
    language_code = Column(String(3))
    country_code = Column(String(3))
    access_provider_code = Column(String(5))
    location_code = Column(String(5))
    publisher_code = Column(String(5))
    licensor_code = Column(String(5))
    copyright_holder_code = Column(String(5))
    data_provider_code = Column(String(5))
    consortium_code = Column(String(5))
    is_suppressed = Column(Boolean)


class ResourceRecordHoldingRecordRelatedLink(Base):
    __tablename__ = 'resource_record_holding_record_related_link'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    resource_record_id = Column(BigInteger)
    holding_record_id = Column(BigInteger)
    resources_display_order = Column(Integer)


class ResourceRecordLicenseRecordLink(Base):
    __tablename__ = 'resource_record_license_record_link'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    resource_record_id = Column(BigInteger)
    license_record_id = Column(BigInteger)
    licenses_display_order = Column(Integer)
    resources_display_order = Column(Integer)


class ResourceRecordOrderRecordLink(Base):
    __tablename__ = 'resource_record_order_record_link'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    resource_record_id = Column(BigInteger)
    order_record_id = Column(BigInteger)
    orders_display_order = Column(Integer)
    resources_display_order = Column(Integer)


class ResourceRecordOrderRecordRelatedLink(Base):
    __tablename__ = 'resource_record_order_record_related_link'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    resource_record_id = Column(BigInteger)
    order_record_id = Column(BigInteger)
    resources_display_order = Column(Integer)


class ResourceView(Base):
    __tablename__ = 'resource_view'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    is_right_result_exact = Column(Boolean)
    rights_code = Column(CHAR(1))
    suppress_code = Column(CHAR(1))
    ecode1 = Column(CHAR(1))
    ecode2 = Column(CHAR(1))
    ecode3 = Column(CHAR(1))
    ecode4 = Column(CHAR(1))
    resource_status_code = Column(CHAR(1))
    package_code = Column(CHAR(1))
    trial_begin_gmt = Column(DateTime(True))
    trial_end_gmt = Column(DateTime(True))
    renewal_gmt = Column(DateTime(True))
    registration_gmt = Column(DateTime(True))
    activation_gmt = Column(DateTime(True))
    edate5_gmt = Column(DateTime(True))
    edate6_gmt = Column(DateTime(True))
    language_code = Column(String(3))
    country_code = Column(String(3))
    access_provider_code = Column(String(5))
    location_code = Column(String(5))
    publisher_code = Column(String(5))
    licensor_code = Column(String(5))
    copyright_holder_code = Column(String(5))
    data_provider_code = Column(String(5))
    consortium_code = Column(String(5))
    is_suppressed = Column(Boolean)
    record_creation_date_gmt = Column(DateTime(True))


class ReturnedBilledItem(Base):
    __tablename__ = 'returned_billed_item'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    patron_record_metadata_id = Column(BigInteger)
    item_cost_amt = Column(Numeric(30, 6))
    checked_in_time_gmt = Column(DateTime(True))
    invoice_number = Column(Integer)


class ScatCategory(Base):
    __tablename__ = 'scat_category'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    code_num = Column(Integer)
    scat_section_id = Column(BigInteger)


class ScatCategoryMyuser(Base):
    __tablename__ = 'scat_category_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(Integer)
    scat_section_id = Column(BigInteger)
    name = Column(String(255))


class ScatCategoryName(Base):
    __tablename__ = 'scat_category_name'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    scat_category_id = Column(BigInteger)
    name = Column(String(255))
    iii_language_code = Column(String(5))


class ScatRange(Base):
    __tablename__ = 'scat_range'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    line_num = Column(Integer)
    start_letter_str = Column(String(100))
    end_letter_str = Column(String(100))
    start_num_str = Column(String(10))
    end_num_str = Column(String(10))
    scat_category_id = Column(BigInteger)
    free_text_type = Column(CHAR(1))


class ScatSection(Base):
    __tablename__ = 'scat_section'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    code_num = Column(Integer)
    index_tag = Column(String(20))


class ScatSectionMyuser(Base):
    __tablename__ = 'scat_section_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(Integer)
    index_tag = Column(String(20))
    name = Column(String(255))


class ScatSectionName(Base):
    __tablename__ = 'scat_section_name'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    scat_section_id = Column(BigInteger)
    name = Column(String(255))
    iii_language_code = Column(String(5))


class SectionRecord(Base):
    __tablename__ = 'section_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    location_code = Column(String(5))
    status_code = Column(CHAR(1))
    program_record_id = Column(BigInteger)
    section_display_order = Column(Integer)
    min_seats = Column(Integer)
    max_seats = Column(Integer)
    reg_open_date_gmt = Column(DateTime)
    reg_close_date_gmt = Column(DateTime)
    ecommerce_code = Column(CHAR(1))
    max_alert_sent_date_gmt = Column(DateTime)
    tickler_sent_date_gmt = Column(DateTime)
    min_alert_sent_date_gmt = Column(DateTime)
    max_waitlist_num = Column(Integer)
    zcode1 = Column(CHAR(1))
    zcode2 = Column(CHAR(1))
    zcode3 = Column(CHAR(1))
    is_suppressed = Column(Boolean)


class SectionRecordSession(Base):
    __tablename__ = 'section_record_session'
    __table_args__ = {'schema': 'sierra_view'}

    section_record_id = Column(BigInteger)
    start_date = Column(DateTime(True))
    duration_minutes = Column(Integer)
    session_display_order = Column(Integer)
    id = Column(BigInteger)
    start_date_str = Column(CHAR(14))


class SectionRegistrationSeat(Base):
    __tablename__ = 'section_registration_seat'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    section_record_id = Column(BigInteger)
    patron_record_id = Column(BigInteger)
    reg_date_gmt = Column(DateTime)
    is_registered = Column(Boolean)
    seat_note = Column(String(255))
    payment_id = Column(BigInteger)
    reg_date = Column(CHAR(14))
    display_order = Column(Integer)


class SectionView(Base):
    __tablename__ = 'section_view'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    location_code = Column(String(5))
    status_code = Column(CHAR(1))
    program_record_id = Column(BigInteger)
    section_display_order = Column(Integer)
    min_seats = Column(Integer)
    max_seats = Column(Integer)
    reg_open_date_gmt = Column(DateTime)
    reg_close_date_gmt = Column(DateTime)
    ecommerce_code = Column(CHAR(1))
    max_alert_sent_date_gmt = Column(DateTime)
    tickler_sent_date_gmt = Column(DateTime)
    min_alert_sent_date_gmt = Column(DateTime)
    max_waitlist_num = Column(Integer)
    zcode1 = Column(CHAR(1))
    zcode2 = Column(CHAR(1))
    zcode3 = Column(CHAR(1))
    is_suppressed = Column(Boolean)


class SessionAttendance(Base):
    __tablename__ = 'session_attendance'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    section_record_session_id = Column(BigInteger)
    section_registration_seat_id = Column(BigInteger)
    patron_record_id = Column(BigInteger)
    total_attended = Column(Integer)


class StatisticGroup(Base):
    __tablename__ = 'statistic_group'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code_num = Column(Integer)
    location_code = Column(String(5))


class StatisticGroupMyuser(Base):
    __tablename__ = 'statistic_group_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(Integer)
    location_code = Column(String(5))
    name = Column(String(255))


class StatisticGroupName(Base):
    __tablename__ = 'statistic_group_name'
    __table_args__ = {'schema': 'sierra_view'}

    statistic_group_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class Subfield(Base):
    __tablename__ = 'subfield'
    __table_args__ = {'schema': 'sierra_view'}

    record_id = Column(BigInteger)
    varfield_id = Column(BigInteger)
    field_type_code = Column(CHAR(1))
    marc_tag = Column(String(3))
    marc_ind1 = Column(CHAR(1))
    marc_ind2 = Column(CHAR(1))
    occ_num = Column(Integer)
    display_order = Column(Integer)
    tag = Column(CHAR(1))
    content = Column(String(20001))


class SubfieldView(Base):
    __tablename__ = 'subfield_view'
    __table_args__ = {'schema': 'sierra_view'}

    record_id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    varfield_id = Column(BigInteger)
    field_type_code = Column(CHAR(1))
    marc_tag = Column(String(3))
    marc_ind1 = Column(CHAR(1))
    marc_ind2 = Column(CHAR(1))
    occ_num = Column(Integer)
    display_order = Column(Integer)
    tag = Column(CHAR(1))
    content = Column(String(20001))


class SuiteBehaviorView(Base):
    __tablename__ = 'suite_behavior_view'
    __table_args__ = {'schema': 'sierra_view'}

    suite = Column(String(20))
    app = Column(String(20))
    code = Column(String(255))
    value = Column(String)
    type = Column(String(255))


class SuiteMessageView(Base):
    __tablename__ = 'suite_message_view'
    __table_args__ = {'schema': 'sierra_view'}

    suite = Column(String(20))
    app = Column(String(20))
    code = Column(String(100))
    lang = Column(String(3))
    value = Column(String(1000))


class SuiteSkinView(Base):
    __tablename__ = 'suite_skin_view'
    __table_args__ = {'schema': 'sierra_view'}

    suite = Column(String(20))
    app = Column(String(20))
    code = Column(String(255))
    lang = Column(String(3))
    type = Column(String(255))
    value = Column(String)


class SystemOptionGroup(Base):
    __tablename__ = 'system_option_group'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code_num = Column(Integer)


class SystemOptionGroupName(Base):
    __tablename__ = 'system_option_group_name'
    __table_args__ = {'schema': 'sierra_view'}

    system_option_group_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class TargetAudience(Base):
    __tablename__ = 'target_audience'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    is_default = Column(Boolean)
    display_order = Column(Integer)


class TargetAudienceMyuser(Base):
    __tablename__ = 'target_audience_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    is_default = Column(Boolean)
    display_order = Column(Integer)
    name = Column(String(255))


class TargetAudienceName(Base):
    __tablename__ = 'target_audience_name'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    name = Column(String(255))
    iii_language_id = Column(Integer)
    target_audience_id = Column(Integer)


class TempLocationProperty(Base):
    __tablename__ = 'temp_location_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(3))
    display_order = Column(Integer)


class TempLocationPropertyMyuser(Base):
    __tablename__ = 'temp_location_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(3))
    display_order = Column(Integer)
    name = Column(String(255))


class TempLocationPropertyName(Base):
    __tablename__ = 'temp_location_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    temp_location_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class TitlePagingReport(Base):
    __tablename__ = 'title_paging_report'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    prepared_date_gmt = Column(DateTime)
    location_type = Column(Integer)
    location_code = Column(String(5))
    location_group_code_num = Column(Integer)
    longname = Column(String(200))


class TitlePagingReportEntry(Base):
    __tablename__ = 'title_paging_report_entry'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    title_paging_report_id = Column(BigInteger)
    record_metadata_id = Column(BigInteger)
    display_order = Column(Integer)
    title = Column(String(200))
    call_number = Column(String(200))
    is_processed = Column(Boolean)


class TitlePagingReportEntryItem(Base):
    __tablename__ = 'title_paging_report_entry_item'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    title_paging_report_entry_id = Column(BigInteger)
    record_metadata_id = Column(BigInteger)
    scanned_date_gmt = Column(DateTime)


class TitlePagingReportEntryPatron(Base):
    __tablename__ = 'title_paging_report_entry_patron'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    title_paging_report_entry_id = Column(BigInteger)
    record_metadata_id = Column(BigInteger)


class TransitBoxRecord(Base):
    __tablename__ = 'transit_box_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    barcode = Column(String(256))
    description = Column(String(256))


class TransitBoxRecordItemRecord(Base):
    __tablename__ = 'transit_box_record_item_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    transit_box_record_id = Column(BigInteger)
    item_record_metadata_id = Column(BigInteger)
    from_location_id = Column(Integer)
    to_location_id = Column(Integer)


class TransitBoxStatu(Base):
    __tablename__ = 'transit_box_status'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    location_id = Column(BigInteger)
    arrival_timestamp = Column(DateTime(True))
    transit_box_record_id = Column(BigInteger)


class UserDefinedAcode1Myuser(Base):
    __tablename__ = 'user_defined_acode1_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedAcode2Myuser(Base):
    __tablename__ = 'user_defined_acode2_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedBcode1Myuser(Base):
    __tablename__ = 'user_defined_bcode1_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedBcode2Myuser(Base):
    __tablename__ = 'user_defined_bcode2_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedBcode3Myuser(Base):
    __tablename__ = 'user_defined_bcode3_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedCategory(Base):
    __tablename__ = 'user_defined_category'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    code = Column(String(255))


class UserDefinedCcode1Myuser(Base):
    __tablename__ = 'user_defined_ccode1_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedCcode2Myuser(Base):
    __tablename__ = 'user_defined_ccode2_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedCcode3Myuser(Base):
    __tablename__ = 'user_defined_ccode3_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedEcode1Myuser(Base):
    __tablename__ = 'user_defined_ecode1_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedEcode2Myuser(Base):
    __tablename__ = 'user_defined_ecode2_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedEcode3Myuser(Base):
    __tablename__ = 'user_defined_ecode3_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedEcode4Myuser(Base):
    __tablename__ = 'user_defined_ecode4_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedGcode1Myuser(Base):
    __tablename__ = 'user_defined_gcode1_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedGcode2Myuser(Base):
    __tablename__ = 'user_defined_gcode2_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedGcode3Myuser(Base):
    __tablename__ = 'user_defined_gcode3_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedIcode1Myuser(Base):
    __tablename__ = 'user_defined_icode1_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedIcode2Myuser(Base):
    __tablename__ = 'user_defined_icode2_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedLcode1Myuser(Base):
    __tablename__ = 'user_defined_lcode1_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedLcode2Myuser(Base):
    __tablename__ = 'user_defined_lcode2_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedLcode3Myuser(Base):
    __tablename__ = 'user_defined_lcode3_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedNcode1Myuser(Base):
    __tablename__ = 'user_defined_ncode1_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedNcode2Myuser(Base):
    __tablename__ = 'user_defined_ncode2_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedNcode3Myuser(Base):
    __tablename__ = 'user_defined_ncode3_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedOcode1Myuser(Base):
    __tablename__ = 'user_defined_ocode1_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedOcode2Myuser(Base):
    __tablename__ = 'user_defined_ocode2_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedOcode3Myuser(Base):
    __tablename__ = 'user_defined_ocode3_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedOcode4Myuser(Base):
    __tablename__ = 'user_defined_ocode4_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedPcode1Myuser(Base):
    __tablename__ = 'user_defined_pcode1_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedPcode2Myuser(Base):
    __tablename__ = 'user_defined_pcode2_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedPcode3Myuser(Base):
    __tablename__ = 'user_defined_pcode3_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedPcode4Myuser(Base):
    __tablename__ = 'user_defined_pcode4_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedProperty(Base):
    __tablename__ = 'user_defined_property'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    user_defined_category_id = Column(Integer)
    code = Column(String(255))
    display_order = Column(Integer)


class UserDefinedPropertyMyuser(Base):
    __tablename__ = 'user_defined_property_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedPropertyName(Base):
    __tablename__ = 'user_defined_property_name'
    __table_args__ = {'schema': 'sierra_view'}

    user_defined_property_id = Column(Integer)
    iii_language_id = Column(Integer)
    name = Column(String(255))


class UserDefinedScode1Myuser(Base):
    __tablename__ = 'user_defined_scode1_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedScode2Myuser(Base):
    __tablename__ = 'user_defined_scode2_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedScode3Myuser(Base):
    __tablename__ = 'user_defined_scode3_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedScode4Myuser(Base):
    __tablename__ = 'user_defined_scode4_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedVcode1Myuser(Base):
    __tablename__ = 'user_defined_vcode1_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedVcode2Myuser(Base):
    __tablename__ = 'user_defined_vcode2_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedVcode3Myuser(Base):
    __tablename__ = 'user_defined_vcode3_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedZcode1Myuser(Base):
    __tablename__ = 'user_defined_zcode1_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedZcode2Myuser(Base):
    __tablename__ = 'user_defined_zcode2_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class UserDefinedZcode3Myuser(Base):
    __tablename__ = 'user_defined_zcode3_myuser'
    __table_args__ = {'schema': 'sierra_view'}

    code = Column(String(255))
    user_defined_category_id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class Varfield(Base):
    __tablename__ = 'varfield'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    varfield_type_code = Column(CHAR(1))
    marc_tag = Column(String(3))
    marc_ind1 = Column(CHAR(1))
    marc_ind2 = Column(CHAR(1))
    occ_num = Column(Integer)
    field_content = Column(String(20001))




class VarfieldTypeName(Base):
    __tablename__ = 'varfield_type_name'
    __table_args__ = {'schema': 'sierra_view'}

    varfield_type_id = Column(BigInteger)
    iii_language_id = Column(BigInteger)
    short_name = Column(String(20))
    name = Column(String(255))


class VarfieldView(Base):
    __tablename__ = 'varfield_view'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    varfield_type_code = Column(CHAR(1))
    marc_tag = Column(String(3))
    marc_ind1 = Column(CHAR(1))
    marc_ind2 = Column(CHAR(1))
    occ_num = Column(Integer)
    field_content = Column(String(20001))


class VendorRecord(Base):
    __tablename__ = 'vendor_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    accounting_unit_code_num = Column(Integer)
    code = Column(String(5))
    claim_cycle_code = Column(CHAR(1))
    vcode1 = Column(CHAR(1))
    vcode2 = Column(CHAR(1))
    vcode3 = Column(CHAR(1))
    order_cnt = Column(Integer)
    claim_cnt = Column(Integer)
    cancel_cnt = Column(Integer)
    receipt_cnt = Column(Integer)
    invoice_cnt = Column(Integer)
    orders_claimed_cnt = Column(Integer)
    copies_received_cnt = Column(Integer)
    order_total_amt = Column(Numeric(30, 6))
    invoice_total_amt = Column(Numeric(30, 6))
    estimated_received_price_amt = Column(Numeric(30, 6))
    estimated_cancelled_price_amt = Column(Numeric(30, 6))
    average_weeks = Column(Integer)
    discount = Column(Integer)
    vendor_message_code = Column(String(3))
    language_code = Column(String(3))
    gir_code = Column(Integer)
    is_suppressed = Column(Boolean)


class VendorRecordAddres(Base):
    __tablename__ = 'vendor_record_address'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    vendor_record_id = Column(BigInteger)
    vendor_record_address_type_id = Column(BigInteger)
    display_order = Column(Integer)
    addr1 = Column(String(1000))
    addr2 = Column(String(1000))
    addr3 = Column(String(1000))
    village = Column(String(1000))
    city = Column(String(1000))
    region = Column(String(1000))
    postal_code = Column(String(100))
    country = Column(String(1000))


class VendorRecordAddressType(Base):
    __tablename__ = 'vendor_record_address_type'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    code = Column(CHAR(1))


class VendorView(Base):
    __tablename__ = 'vendor_view'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    accounting_unit_code_num = Column(Integer)
    code = Column(String(5))
    claim_cycle_code = Column(CHAR(1))
    vcode1 = Column(CHAR(1))
    vcode2 = Column(CHAR(1))
    vcode3 = Column(CHAR(1))
    order_cnt = Column(Integer)
    claim_cnt = Column(Integer)
    cancel_cnt = Column(Integer)
    receipt_cnt = Column(Integer)
    invoice_cnt = Column(Integer)
    orders_claimed_cnt = Column(Integer)
    copies_received_cnt = Column(Integer)
    order_total_amt = Column(Numeric(30, 6))
    invoice_total_amt = Column(Numeric(30, 6))
    estimated_received_price_amt = Column(Numeric(30, 6))
    estimated_cancelled_price_amt = Column(Numeric(30, 6))
    average_weeks = Column(Integer)
    discount = Column(Integer)
    vendor_message_code = Column(String(3))
    language_code = Column(String(3))
    gir_code = Column(Integer)
    is_suppressed = Column(Boolean)
    record_creation_date_gmt = Column(DateTime(True))


class VolumeRecord(Base):
    __tablename__ = 'volume_record'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_id = Column(BigInteger)
    sort_order = Column(Integer)
    is_suppressed = Column(Boolean)


class VolumeRecordItemRecordLink(Base):
    __tablename__ = 'volume_record_item_record_link'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    volume_record_id = Column(BigInteger)
    item_record_id = Column(BigInteger)
    items_display_order = Column(Integer)


class VolumeView(Base):
    __tablename__ = 'volume_view'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    record_type_code = Column(CHAR(1))
    record_num = Column(Integer)
    sort_order = Column(Integer)
    is_suppressed = Column(Boolean)
    record_creation_date_gmt = Column(DateTime(True))


class Wamreport(Base):
    __tablename__ = 'wamreport'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(BigInteger)
    logged_gmt = Column(DateTime(True))
    requesting_ip = Column(String(32))
    requesting_port = Column(Integer)
    requesting_iii_name = Column(String(255))
    dest_port = Column(Integer)
    dest_code = Column(String(8))
    response_category_code_num = Column(Integer)
    patron_record_metadata_id = Column(BigInteger)
    ptype_code_num = Column(Integer)
    pcode1 = Column(CHAR(1))
    pcode2 = Column(CHAR(1))
    pcode3_code_num = Column(Integer)
    pcode4_code_num = Column(Integer)
    rejection_reason_code_num = Column(Integer)


class Workflow(Base):
    __tablename__ = 'workflow'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    display_order = Column(Integer)
    name = Column(String(255))


class WorkflowFunction(Base):
    __tablename__ = 'workflow_function'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    workflow_id = Column(Integer)
    function_id = Column(Integer)
    display_order = Column(Integer)


class WorkflowName(Base):
    __tablename__ = 'workflow_name'
    __table_args__ = {'schema': 'sierra_view'}

    workflow_id = Column(Integer)
    iii_language_id = Column(Integer)
    menu_name = Column(String(255))


class ZipCodeInfo(Base):
    __tablename__ = 'zip_code_info'
    __table_args__ = {'schema': 'sierra_view'}

    id = Column(Integer)
    zip_code = Column(String(32))
    latitude = Column(String(32))
    longitude = Column(String(32))
    country_code = Column(String(32))



