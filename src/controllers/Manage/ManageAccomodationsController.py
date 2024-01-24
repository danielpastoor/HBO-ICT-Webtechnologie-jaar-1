""" Index Controller
"""
# needed imports
from flask import render_template, request, flash, redirect
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

# own imports
from src.controllers.Base.ControllerBase import ControllerBase, RouteMethods
from src.data.ApplicationContext import ApplicationContext
from src.models.AccommodationEntity import AccommodationEntity


class ManageAccommodationController(ControllerBase):

    def __init__(self):
        self.app_context = ApplicationContext()

    @login_required
    def index(self):
        accommodations = self.app_context.get_all_accommodations_manage()

        return render_template("pages/manage/manage-accommodation.html", accommodations=accommodations)

    @login_required
    def post(self):
        """ Handle the form submission for adding new accommodation. """

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
        if self.app_context.add_accommodation(accommodation_data):
            flash("Accommodation added successfully.", "success")
        else:
            flash("Failed to add accommodation.", "error")

        return redirect('/manage/accommodations')

    @login_required
    def delete_accommodation(self, id):
        if not current_user.is_admin:
            flash("Je hebt hier niet genoeg rechten voor.", "error")
            return redirect('/manage/accommodations')  # Redirect to a safe page

        if self.__delete_accommodation(id):
            flash("Accommodatie is verwijderd.", "success")
        else:
            flash("Accommodatie verwijderen faalt.", "error")

        return redirect('/manage/accommodations')  # Redirect to the users list page

    def __delete_accommodation(self, id):
        """
        Delete an accommodation from the database.
        """
        try:
            self.app_context.Delete(AccommodationEntity(), id)
            return True
        except Exception as e:
            print(f"Error removing accommodation: {e}")
            return False

    @RouteMethods(["GET", "POST"])
    @login_required
    def edit(self, id):
        if request.method == "GET":
            # Fetch user details for editing
            accommodation_to_edit = self.app_context.First(AccommodationEntity(), condition=f"id = {id}")

            if not accommodation_to_edit:
                flash("Accommodation not found.", "error")
                return redirect('/manage/accommodations')  # Adjust as per your route naming

            return render_template("pages/manage/manage-edit-accommodation.html",
                                   accommodation=accommodation_to_edit)

        elif request.method == "POST":
            # Extract form data
            name = request.form['name']
            description = request.form['description']
            location = request.form['location']
            price = request.form['price']
            max_persons = request.form['max_persons']

            # Create accommodation data dictionary
            accommodation_data = {
                "name": name,
                "description": description,
                "location": location,
                "price": price,
                "max_persons": max_persons,
            }

            # Add accommodation to the database
            self.app_context.Update(AccommodationEntity(), accommodation_data, id)

            flash("Accommodatie is geupdate.", "success")

            return redirect('/manage/accommodations')  # Redirect to the users list page


if __name__ == "__main__":
    pass
