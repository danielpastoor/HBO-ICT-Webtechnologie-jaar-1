""" Index Controller
"""
# needed imports
from flask import render_template, request, flash, redirect
from flask_login import login_required
from werkzeug.utils import secure_filename

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext


class ManageAccommodationController(ControllerBase):

    @login_required
    def index(self):
        app_context = ApplicationContext()
        accommodations = app_context.get_all_accommodations_manage()

        return render_template("pages/dashboard/manageaccommodation.html", accommodations=accommodations)


class AddAccommodationController(ControllerBase):

    @login_required
    def get(self):
        """ Render the form for adding new accommodation. """
        return render_template("pages/dashboard/addaccommodation.html")

    @login_required
    def post(self):
        """ Handle the form submission for adding new accommodation. """
        app_context = ApplicationContext()

        # Extract form data
        name = request.form['name']
        description = request.form['description']
        location = request.form['location']
        price = request.form['price']
        max_persons = request.form['max_persons']

        # Process thumbnail image
        thumbnail_image = request.files['thumbnail_image']
        thumbnail_filename = secure_filename(thumbnail_image.filename)
        thumbnail_image.save('src/static/img/' + thumbnail_filename)

        # Process additional images
        images_files = request.files.getlist('images')
        images_filenames = [secure_filename(img.filename) for img in images_files]
        for img_file in images_files:
            img_file.save('src/static/img/' + secure_filename(img_file.filename))
        images_str = ','.join(images_filenames)

        # Create accommodation data dictionary
        accommodation_data = {
            "name": name,
            "description": description,
            "location": location,
            "price": price,
            "max_persons": max_persons,
            "thumbnail_image": thumbnail_filename,
            "images": images_str
        }

        # Add accommodation to the database
        if app_context.add_accommodation(accommodation_data):
            flash("Accommodation added successfully.", "success")
        else:
            flash("Failed to add accommodation.", "error")

        return redirect('/manage_accommodations/')


if __name__ == "__main__":
    pass
