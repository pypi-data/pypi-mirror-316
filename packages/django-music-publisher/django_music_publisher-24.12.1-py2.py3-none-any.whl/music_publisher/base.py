"""Contains base (abstract) classes used in :mod:`.models`
"""

import base64
import re
from uuid import uuid4

import django.core.exceptions
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .societies import SOCIETIES
from .validators import CWRFieldValidator


def upload_to(instance, filename):
    ext = filename.rsplit(".", 1)[-1]
    folder = instance._meta.model_name
    uuid = uuid4().bytes
    b64 = base64.urlsafe_b64encode(uuid)
    fn = b64.rstrip(b"=").decode()
    return f"{folder}/{fn}.{ext}"


class NotesManager(models.Manager):
    """Manager for objects inheriting from :class:`NotesBase`.

    Defers :attr:`NotesBase.notes` field.
    """

    def get_queryset(self):
        """Defer :attr:`NotesBase.notes` field."""
        qs = super().get_queryset()
        qs = qs.defer("notes")
        return qs


class NotesBase(models.Model):
    """Abstract class for all classes that have notes.

    Attributes:
        notes (django.db.models.TextField): Notes, free internal text field
    """

    class Meta:
        abstract = True

    objects = NotesManager()

    notes = models.TextField(blank=True)


class DescriptionBase(models.Model):
    """Abstract class for all classes that have publicly visible descriptions.

    Attributes:
        description (django.db.models.TextField): Public description
    """

    class Meta:
        abstract = True

    description = models.TextField(blank=True)


class TitleBase(models.Model):
    """Abstract class for all classes that have a title.

    Attributes:
        title (django.db.models.CharField): Title, used in work title,
            alternate title, etc.
    """

    class Meta:
        abstract = True

    TITLE_TYPES = (
        ("AT", "Alternative Title"),
        ("TE", "First Line of Text"),
        ("FT", "Formal Title"),
        ("IT", "Incorrect Title"),
        # ("OT", "Original Title"),
        # ("TT", "Original Title Translated"),
        ("ET", "Extra Search Title"),
    )

    title_type = models.CharField(
        max_length=2, choices=TITLE_TYPES, default="AT"
    )
    title = models.CharField(
        max_length=60, db_index=True, validators=(CWRFieldValidator("title"),)
    )

    def __str__(self):
        return self.title


class PersonBase(models.Model):
    """Base class for all classes that contain people with first and last name.

    This includes writers and artists. For bands, only the last name field is
    used.

    Attributes:
        first_name (django.db.models.CharField): First Name
        last_name (django.db.models.CharField): Last Name
    """

    class Meta:
        abstract = True

    first_name = models.CharField(
        max_length=30, blank=True, validators=(CWRFieldValidator("name"),)
    )
    last_name = models.CharField(
        max_length=45, db_index=True, validators=(CWRFieldValidator("name"),)
    )
    image = models.ImageField(max_length=255, upload_to=upload_to, blank=True)

    def __str__(self):
        if self.first_name:
            return "{0.first_name} {0.last_name}".format(self).upper()
        return self.last_name.upper()


class SocietyAffiliationBase(models.Model):
    """Abstract base for all objects with CMO affiliations

    Attributes:
        pr_society (django.db.models.CharField):
            Performing Rights Society Code
        mr_society (django.db.models.CharField):
            Mechanical Rights Society Code
        sr_society (django.db.models.CharField):
            Sync. Rights Society Code
    """

    class Meta:
        abstract = True

    pr_society = models.CharField(
        "Performance rights society",
        max_length=3,
        blank=True,
        null=True,
        choices=SOCIETIES + [("99", "NO SOCIETY")],
    )
    mr_society = models.CharField(
        "Mechanical rights society",
        max_length=3,
        blank=True,
        null=True,
        choices=SOCIETIES,
    )
    sr_society = models.CharField(
        "Synchronization rights society",
        max_length=3,
        blank=True,
        null=True,
        choices=SOCIETIES,
    )


class IPIBase(models.Model):
    """Abstract base for all objects containing IPI numbers.

    Attributes:
        ipi_base (django.db.models.CharField): IPI Base Number
        ipi_name (django.db.models.CharField): IPI Name Number
        _can_be_controlled (django.db.models.BooleanField):
            used to determine if there is enough data for a writer
            to be controlled.
    """

    class Meta:
        abstract = True

    ipi_name = models.CharField(
        "IPI name #",
        max_length=11,
        blank=True,
        null=True,
        unique=True,
        validators=(CWRFieldValidator("ipi_name"),),
    )
    ipi_base = models.CharField(
        "IPI base #",
        max_length=15,
        blank=True,
        null=True,
        validators=(CWRFieldValidator("ipi_base"),),
    )

    _can_be_controlled = models.BooleanField(
        verbose_name="Can be controlled", editable=False, default=False
    )

    def clean_fields(self, *args, **kwargs):
        """
        Data cleanup, allowing various import formats to be converted into
        consistently formatted data.
        """
        if self.ipi_name:
            self.ipi_name = self.ipi_name.zfill(11)
        if self.ipi_base:
            self.ipi_base = self.ipi_base.replace(".", "").upper()
            self.ipi_base = re.sub(
                r"(I).?(\d{9}).?(\d)", r"\1-\2-\3", self.ipi_base
            )
        return super().clean_fields(*args, **kwargs)


class IPIWithGeneralAgreementBase(IPIBase, SocietyAffiliationBase):
    """Abstract base for all objects with general agreements.

    Attributes:
        saan (django.db.models.CharField):
            Society-assigned agreement number, in this context it is used for
            general agreements, for specific agreements use
            :attr:`.models.WriterInWork.saan`.
        generally_controlled (django.db.models.BooleanField):
            flags if a writer is generally controlled (in all works)
        publisher_fee (django.db.models.DecimalField):
            this field is used in calculating publishing fees
    """

    class Meta:
        abstract = True

    saan = models.CharField(
        "SAAN",
        help_text="Use this field for a general original publishing "
        "agreement.",
        validators=(CWRFieldValidator("saan"),),
        max_length=14,
        blank=True,
        null=True,
    )

    generally_controlled = models.BooleanField(
        "General agreement", default=False
    )
    publisher_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def clean(self):
        """Clean the data and validate."""

        self._can_be_controlled = bool(self.ipi_name) & bool(self.pr_society)
        if self.ipi_name == "00000000000":
            self.ipi_name = None
        if self.pr_society == "99":
            self.pr_society = None

        d = {}
        if not self.generally_controlled:
            if self.saan:
                d["saan"] = "Only for a general agreement."
            if self.publisher_fee:
                d["publisher_fee"] = "Only for a general agreement."
        else:
            if not self._can_be_controlled:
                d["generally_controlled"] = (
                    "IPI name number and PR society fields are required for "
                    'a controlled writer. See "Writers" in the user manual.'
                )
        if d:
            raise django.core.exceptions.ValidationError(d)

    def clean_fields(self, *args, **kwargs):
        """
        Data cleanup, allowing various import formats to be converted into
        consistently formatted data.
        """
        if self.saan:
            self.saan = self.saan.upper()  # only in CWR, uppercase anyway
        super().clean_fields(*args, **kwargs)


class AccountNumberBase(models.Model):
    """Abstract base for all objects with an account number.

    Attributes:
        account_number (django.db.models.CharField):
            account number, used for royalty processing
    """

    class Meta:
        abstract = True

    account_number = models.CharField(
        "Account #",
        help_text="Use this field for linking royalty statements with your "
        "accounting.",
        max_length=100,
        blank=True,
        null=True,
    )

    def clean_fields(self, *args, **kwargs):
        """Account Number cleanup"""
        if self.account_number:
            self.account_number = self.account_number.strip()
        return models.Model.clean_fields(self, *args, **kwargs)


class ArtistBase(PersonBase, NotesBase, DescriptionBase):
    """Performing artist base class.

    Attributes:
        isni (django.db.models.CharField): International Standard Name Id
    """

    class Meta:
        verbose_name = "Performing Artist"
        verbose_name_plural = "Performing Artists"
        ordering = ("last_name", "first_name", "-id")
        abstract = True

    isni = models.CharField(
        "ISNI",
        max_length=16,
        blank=True,
        null=True,
        unique=True,
        validators=(CWRFieldValidator("isni"),),
    )

    def clean_fields(self, *args, **kwargs):
        """ISNI cleanup"""
        if self.isni:
            self.isni = self.isni.rjust(16, "0").upper()
        return models.Model.clean_fields(self, *args, **kwargs)


class WriterBase(
    PersonBase,
    IPIWithGeneralAgreementBase,
    NotesBase,
    DescriptionBase,
    AccountNumberBase,
):
    """Base class for writers."""

    class Meta:
        ordering = ("last_name", "first_name", "ipi_name", "-id")
        verbose_name_plural = "Writers"
        abstract = True


class LabelBase(NotesBase, DescriptionBase):
    """Music Label base class.

    Attributes:
        name (django.db.models.CharField): Label Name
    """

    class Meta:
        verbose_name_plural = "Music Labels"
        ordering = ("name",)
        abstract = True

    name = models.CharField(
        max_length=60, unique=True, validators=(CWRFieldValidator("name"),)
    )
    image = models.ImageField(
        "Logo", max_length=255, upload_to=upload_to, blank=True
    )


class LibraryBase(models.Model):
    """Music Library base class.

    Attributes:
        name (django.db.models.CharField): Library Name
    """

    class Meta:
        verbose_name_plural = "Music Libraries"
        ordering = ("name",)
        abstract = True

    name = models.CharField(
        max_length=60, unique=True, validators=(CWRFieldValidator("name"),)
    )


class ReleaseBase(DescriptionBase):
    """Music Release base class

    Attributes:
        cd_identifier (django.db.models.CharField): CD Identifier, used when \
        origin is library
        library (django.db.models.CharField): Library Name
        release_date (django.db.models.DateField): Date of the release
        ean (django.db.models.CharField): EAN code
        release_label (django.db.models.CharField): Label Name
        release_title (django.db.models.CharField): Title of the release
    """

    class Meta:
        ordering = ("release_title", "cd_identifier", "-id")
        abstract = True

    cd_identifier = models.CharField(
        "CD identifier",
        max_length=15,
        blank=True,
        null=True,
        unique=True,
        validators=(CWRFieldValidator("name"),),
    )
    release_date = models.DateField(blank=True, null=True)
    release_title = models.CharField(
        "Release (album) title ",
        max_length=60,
        blank=True,
        null=True,
        validators=(CWRFieldValidator("title"),),
    )
    ean = models.CharField(
        "Release (album) EAN",
        max_length=13,
        blank=True,
        null=True,
        unique=True,
        validators=(CWRFieldValidator("ean"),),
    )
    image = models.ImageField(
        "Cover Art", max_length=255, upload_to=upload_to, blank=True
    )
