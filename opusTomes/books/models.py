from django.contrib.auth.models import User
from django.db import models
from opusTomes.models import BaseModel
from fpdf import FPDF


class Book(BaseModel):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return "Book"


class SRDPage(BaseModel):
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=400)
    casting_time = models.CharField(max_length=100)
    casting_range = models.CharField(max_length=100)
    components = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title + ' - ' + self.sub_title

    def save_as_dnd(self, book):
        dndPage = DNDPage(
                    title = self.title,
                    sub_title =self.sub_title,
                    casting_time = self.casting_time,
                    casting_range = self.casting_range,
                    components = self.components,
                    duration = self.duration,
                    description = self.description,
                    book= book,
                    order= book.pages.count()
                    )
        dndPage.save()


class DNDPage(SRDPage):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="pages")
    order = models.IntegerField()
    pdf_path = models.CharField(max_length=200, blank=True)

    def add_page_to_pdf(self, pdf):
        pdf.add_page()

        # Add the title
        pdf.set_font('theano', '', 16)
        pdf.cell(40, 10, self.title)

        # Add subtitle
        pdf.ln(5)
        pdf.set_font('Arial', '', 10)
        pdf.cell(40, 10, self.sub_title)

        # Add duration
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(23,10, "Casting time: ")
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 10, self.casting_time)

        # Add Range
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(14,10, "Range: ")
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 10, self.casting_range)

        # Add Components
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(25,10, "Components: ")
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 10, self.components)

        # Add Duration
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(25,10, "Duration: ")
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 10, self.duration)

        # Add Desctription
        pdf.ln(5)
        pdf.set_font('theano', '', 10)
        pdf.cell(0, 10, self.description)

