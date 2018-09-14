import tkinter as tk
import pymysql
import museum as db


def popupBox(title, errorTxt):
    popup = tk.Tk()
    popup.geometry("300x300")
    popup.wm_title(title)
    tk.Label(popup, text=errorTxt).grid(row=0, column=0)
    tk.Button(popup, text="Okay", command=popup.destroy).grid(row=1, column=0)
    popup.mainloop()


user = "none"
mName = "none"
isCurator = False
wasCurator = False


class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)  # inhereted class

        # container where the frames are held aka the other screens
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # dictionary of the frames

        # for loop that contains all the frames

        for F in (LoginPage, CreateNewUser, HomePage, AllMuseums, MyTickets, MyReviews, ManageAccount, AdminPage,
                  AcceptCurators, AddMuseums, DeleteMuseums, MuseumReviews, ReviewMuseum, SpecificMAllReviews,
                  CreateCuratorRequest, CuratorHomePage, CuratorMuseums, AddExhibit, CuratorSpecificMuseums):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.update()
        frame.tkraise()


class CreateNewUser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="New User Registration").grid(row=0, column=1)
        tk.Label(self, text="Email:").grid(row=200, column=0)
        tk.Label(self, text="Password:").grid(row=201, column=0)
        tk.Label(self, text="Confirm Password:").grid(row=202, column=0)
        tk.Label(self, text="Credit Card Number:").grid(row=203, column=0)
        tk.Label(self, text="CC Expiration Month:").grid(row=204, column=0)
        tk.Label(self, text="CC Expiration Year:").grid(row=205, column=0)
        tk.Label(self, text="Credit Card Security Code:").grid(row=206, column=0)

        self.e1 = tk.Entry(self)
        self.e1.grid(row=200, column=1)
        self.e2 = tk.Entry(self)
        self.e2.grid(row=201, column=1)
        self.e2.config(show="*")
        self.e3 = tk.Entry(self)
        self.e3.grid(row=202, column=1)
        self.e3.config(show="*")
        self.e4 = tk.Entry(self)
        self.e4.grid(row=203, column=1)
        self.e4.config(show="*")
        self.e5 = tk.Entry(self)
        self.e5.grid(row=204, column=1)
        self.e6 = tk.Entry(self)
        self.e6.grid(row=205, column=1)
        self.e7 = tk.Entry(self)
        self.e7.grid(row=206, column=1)
        self.controller = controller
        button1 = tk.Button(self, text="Create New User",
                            command=lambda: self.properHomeScreen(self.controller)).grid(row=300, column=1)

        button2 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(LoginPage
                                                                  )).grid(row=301, column=1)

    def properHomeScreen(self, controller):
        self.createUser(controller)
        global isCurator
        isCurator = False
        if(isCurator):
            controller.show_frame(CuratorHomePage)
        else:
            controller.show_frame(HomePage)
    def update(self):
        # only for generality
        return

    def createUser(self, controller):
        global user
        if (self.e2.get() == self.e3.get()):
            check = db.createnewaccount(self.e1.get(), self.e2.get(), self.e4.get(), self.e5.get(), self.e6.get(),
                                        self.e7.get())
            if check == 0:
                popupBox("Error", "Email is already being Used!")
            user = self.e1.get()

            self.e1.delete(0, 'end')
            self.e2.delete(0, 'end')
            self.e3.delete(0, 'end')
            self.e4.delete(0, 'end')
            self.e5.delete(0, 'end')
            self.e6.delete(0, 'end')
            self.e7.delete(0, 'end')
            controller.show_frame(HomePage)
        else:
            popupBox("Incorrect Password", "Your Passwords do not match!")


class LoginPage(tk.Frame):  # function
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # labels
        tk.Label(self, text="BMTRS").grid(row=0, column=150)
        tk.Label(self, text="Email:").grid(row=200, column=149)
        tk.Label(self, text="Password:").grid(row=201, column=149)
        # entry boxes
        self.e1 = tk.Entry(self)
        self.e2 = tk.Entry(self)
        self.e2.config(show="*")  # password entry box
        self.e1.grid(row=200, column=150)
        self.e2.grid(row=201, column=150)
        # swap pages

        button1 = tk.Button(self, text="Login",
                            command=lambda: self.getLogin(controller)).grid(row=380, column=150)

        button2 = tk.Button(self, text="Create New User",
                            command=lambda: controller.show_frame(CreateNewUser)).grid(row=400, column=150)

    # check if login is valid
    def getLogin(self, controller):
        success = db.login(self.e1.get(), self.e2.get())
        global user
        global isCurator
        if (success == 1):
            isCurator = False
            user = self.e1.get()
            self.e1.delete(0, 'end')
            self.e2.delete(0, 'end')
            controller.show_frame(HomePage)
        elif (success == 2):

            user = self.e1.get()
            self.e1.delete(0, 'end')
            self.e2.delete(0, 'end')
            controller.show_frame(AdminPage)
        elif (success == 3):
            user = self.e1.get()
            isCurator = True
            self.e1.delete(0, 'end')
            self.e2.delete(0, 'end')
            controller.show_frame(CuratorHomePage)
        else:
            popupBox("Incorrect Username/Password", "You're Username/Password is Incorrect")


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # labels
        global user
        global isCurator
        self.l1 = tk.Label(self, text="Welcome, " + user + "!")
        self.l1.grid(row=0, column=150)

        museums = db.allmuseums()
        ind = 0;
        Mlist = [];
        self.var = tk.StringVar()
        self.var.set('Museums')

        for m in museums:
            museum = m['museum_name']
            if (museum != ""''""):
                Mlist.insert(ind, museum)
            ind = ind + 1
        self.l2 = tk.Label(self, text="Choose a Museum:")
        self.l2.grid(row=399, column=0)
        self.o = tk.OptionMenu(self, self.var, *Mlist, command=print(self.var.get()))
        self.o.grid(row=399, column=150)
        self.b1 = tk.Button(self, text="Go", command=lambda: self.setUniversalMuseum(controller)).grid(row=399,
                                                                                                       column=151)
        self.b5 = tk.Button(self, text="All Museums",
                            command=lambda: controller.show_frame(AllMuseums))
        self.b5.grid(row=400, column=150)
        self.b2 = tk.Button(self, text="My Tickets",
                            command=lambda: controller.show_frame(MyTickets))
        self.b2.grid(row=401, column=150)
        self.b3 = tk.Button(self, text="My Reviews",
                            command=lambda: controller.show_frame(MyReviews))
        self.b3.grid(row=402, column=150)

        self.b4 = tk.Button(self, text="Manage Account",
                            command=lambda: controller.show_frame(ManageAccount))
        self.b4.grid(row=403, column=150)
        self.controller = controller

    def update(self):
        self.l1.grid_forget()
        self.l1 = tk.Label(self, text="Welcome, " + user + "!")
        self.l1.grid(row=0, column=150)

        self.o.grid_forget()
        museums = db.allmuseums()
        ind = 0;
        Mlist = [];
        for m in museums:
            museum = m['museum_name']
            if (museum != ""''""):
                Mlist.insert(ind, museum)
            ind = ind + 1
        self.var.set("Musuem")
        self.o = tk.OptionMenu(self, self.var, *Mlist, command=print(self.var.get()))
        self.o.grid(row=399, column=150)
       

    def setUniversalMuseum(self, controller):
        global mName
        global isCurator

        mName = self.var.get()
        if (isCurator):
            controller.show_frame(CuratorSpecificMuseums)
        else:

            controller.show_frame(MuseumReviews)
class CuratorHomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # labels
        global user
        global isCurator
        self.l1 = tk.Label(self, text="Welcome, " + user + "!")
        self.l1.grid(row=0, column=150)

        museums = db.allmuseums()
        ind = 0;
        Mlist = [];
        self.var = tk.StringVar()
        self.var.set('Museums')

        for m in museums:
            museum = m['museum_name']
            if (museum != ""''""):
                Mlist.insert(ind, museum)
            ind = ind + 1
        self.l2 = tk.Label(self, text="Choose a Museum:")
        self.l2.grid(row=399, column=0)
        self.o = tk.OptionMenu(self, self.var, *Mlist, command=print(self.var.get()))
        self.o.grid(row=399, column=150)
        self.b1 = tk.Button(self, text="Go", command=lambda: self.setUniversalMuseum(controller)).grid(row=399,
                                                                                                       column=151)
        self.b5 = tk.Button(self, text="All Museums",
                            command=lambda: controller.show_frame(AllMuseums))
        self.b5.grid(row=400, column=150)
        self.b2 = tk.Button(self, text="My Tickets",
                            command=lambda: controller.show_frame(MyTickets))
        self.b2.grid(row=401, column=150)
        self.b3 = tk.Button(self, text="My Reviews",
                            command=lambda: controller.show_frame(MyReviews))
        self.b3.grid(row=402, column=150)

        self.b4 = tk.Button(self, text="Manage Account",
                            command=lambda: controller.show_frame(ManageAccount))
        self.b4.grid(row=403, column=150)
        self.b6 = tk.Button(self, text="My Museums",
                                command=lambda: self.controller.show_frame(CuratorMuseums))
        self.b6.grid(row=404, column=150)

        self.controller = controller

    def update(self):
        self.l1.grid_forget()
        self.l1 = tk.Label(self, text="Welcome, " + user + "!")
        self.l1.grid(row=0, column=150)

        self.o.grid_forget()
        museums = db.allmuseums()
        ind = 0;
        Mlist = [];
        for m in museums:
            museum = m['museum_name']
            if (museum != ""''""):
                Mlist.insert(ind, museum)
            ind = ind + 1
        self.var.set("Musuem")
        self.o = tk.OptionMenu(self, self.var, *Mlist, command=print(self.var.get()))
        self.o.grid(row=399, column=150)
       

    def setUniversalMuseum(self, controller):
        global mName
        global isCurator
        mName = self.var.get()
        if (isCurator):
            controller.show_frame(CuratorSpecificMuseums)
        else:

            controller.show_frame(MuseumReviews)



class MuseumReviews(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global mName
        self.controller = controller
        self.l1 = tk.Label(self, text="Welcome to the: " + mName + "!")
        self.l1.grid(row=0, column=300)
        tk.Label(self, text="Exhibit").grid(row=1, column=201)
        tk.Label(self, text="Year").grid(row=1, column=300)
        tk.Label(self, text="Url").grid(row=1, column=450)
        exhibits = db.viewspecificmuseum(mName)
        ind = 0;
        eList = [];
        yList = [];
        uList = [];
        for e in exhibits:
            exhibit = e['exhibit_name']
            if (exhibit != ""''""):
                eList.insert(ind, exhibit)
            ind = ind + 1
        ind = 0
        for y in exhibits:
            year = y['year']
            yList.insert(ind, year)
            ind = ind + 1
        ind = 0
        for u in exhibits:
            url = u['url']
            uList.insert(ind, url)
            ind = ind + 1

        ind = 1

        self.LabelList = []
        self.LabelList.append(self.l1)
        labInd = 0
        for m in eList:
            self.l = tk.Label(self, text=m)
            self.l.grid(row=2 + ind, column=201)
            self.LabelList.append(self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for d in yList:
            self.l = tk.Label(self, text=d)
            self.l.grid(row=2 + ind, column=300)
            self.LabelList.append(self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for p in uList:
            self.l1 = tk.Label(self, text=p)
            self.l1.grid(row=2 + ind, column=450)
            self.LabelList.append(self.l)
            labInd = labInd + 1
            ind = ind + 1
        tk.Button(self, text="Purchase Ticket",
                  command=lambda: self.purchaseTicket()).grid(row=300 + ind, column=300)
        tk.Button(self, text="Review Museum",
                  command=lambda: controller.show_frame(ReviewMuseum)).grid(row=301 + ind, column=300)
        tk.Button(self, text="View Other Reviews",
                  command=lambda: controller.show_frame(SpecificMAllReviews)).grid(row=302 + ind, column=300)
        tk.Button(self, text="Back",
                  command=lambda: self.properHomeScreen(controller)).grid(row=350 + ind, column=0)

    def properHomeScreen(self, controller):
        global isCurator
        if(isCurator):
            controller.show_frame(CuratorHomePage)
        else:
            controller.show_frame(HomePage)
            
    def purchaseTicket(self):
        museum = "test"
        check = db.purchaseticket(user, mName)
        if (check == 1):
            popupBox("Success", "Thank You for Purchasing a Ticket to the " + mName)
        elif (check == 4):
            popupBox("Error", "You already bought a ticket to " + mName)

    def update(self):
        global mName
        for l in self.LabelList:
            l.grid_forget()
        self.l1 = tk.Label(self, text="Welcome to the: " + mName + "!")
        self.l1.grid(row=0, column=300)


        exhibits = db.viewspecificmuseum(mName)
        ind = 0;
        eList = [];
        yList = [];
        uList = [];
        for e in exhibits:
            exhibit = e['exhibit_name']
            if (exhibit != ""''""):
                eList.insert(ind, exhibit)
            ind = ind + 1
        ind = 0
        for y in exhibits:
            year = y['year']
            yList.insert(ind, year)
            ind = ind + 1
        ind = 0
        for u in exhibits:
            url = u['url']
            uList.insert(ind, url)
            ind = ind + 1

        ind = 1

        self.LabelList = []
        self.LabelList.append(self.l1)
        labInd = 0
        for m in eList:
            self.l = tk.Label(self, text=m)
            self.l.grid(row=2 + ind, column=201)
            self.LabelList.append(self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for d in yList:
            self.l = tk.Label(self, text=d)
            self.l.grid(row=2 + ind, column=300)
            self.LabelList.append(self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for p in uList:
            self.l = tk.Label(self, text=p)
            self.l.grid(row=2 + ind, column=450)
            self.LabelList.append(self.l)
            labInd = labInd + 1
            ind = ind + 1

class ReviewMuseum(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global mName
        tk.Label(self, text="Write a Review for " + mName + "!").grid(row=0, column=150)
        tk.Label(self, text="Write Your Review Here:").grid(row=2, column=0)
        tk.Label(self, text="Rating*:").grid(row=1, column=0)

        var = tk.IntVar()
        var.set(3)
        list = [1, 2, 3, 4, 5]
        tk.OptionMenu(self, var, *list, command=print(var.get())).grid(row=1, column=150)
        self.e = tk.Entry(self);
        self.e.grid(row=2, column=150);

        tk.Button(self, text="Submit Review",
                  command=lambda: var.set(self.submit(var.get()))).grid(row=3, column=150)
        tk.Button(self, text="Back",
                  command=lambda: controller.show_frame(MuseumReviews)).grid(row=4, column=150)

    def submit(self, rating):
        check = db.reviewmuseum(user, mName, self.e.get(), rating)
        if (check == 3):
            popupBox("Error", "You have already Left a Review")
        self.e.delete(0, 'end')
        return 3


class SpecificMAllReviews(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global mName
        tk.Label(self, text="All Reviews").grid(row=0, column=150)
        tk.Label(self, text="Comment").grid(row=1, column=0)
        tk.Label(self, text="Rating").grid(row=1, column=300)

        review = db.viewmuseumreview(mName)

        ind = 0;
        cList = [];
        rList = [];
        for c in review:
            comment = c['comment']
            cList.insert(ind, comment)
            ind = ind + 1
        ind = 0
        for r in review:
            rating = r['rating']
            rList.insert(ind, rating)
            ind = ind + 1
        ind = 2

        self.LabelList = []
        labInd = 0
        for c in cList:
            self.l = tk.Label(self, text=c)
            self.l.grid(row=ind, column=0)
            self.l.grid(row=2 + ind, column=201)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 2
        for r in rList:
            self.l = tk.Label(self, text=str(r) + "/5")
            self.l.grid(row=ind, column=300)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        self.controller = controller
        self.b = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame(MuseumReviews))
        self.b.grid(row=ind, column=150)


    def update(self):
        global mName

        for l in self.LabelList:
            l.grid_forget()
        self.b.grid_forget()
        review = db.viewmuseumreview(mName)
        ind = 0
        cList = []
        rList = []
        for c in review:
            comment = c['comment']
            cList.insert(ind, comment)
            ind = ind + 1
        ind = 0
        for r in review:
            rating = r['rating']
            rList.insert(ind, rating)
            ind = ind + 1
        ind = 2

        self.LabelList = []
        labInd = 0
        for c in cList:
            self.l = tk.Label(self, text=c)
            self.l.grid(row=ind, column=0)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1

        ind = 2
        for r in rList:
            self.l = tk.Label(self, text=str(r) + "/5")
            self.l.grid(row=ind, column=300)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        self.b = tk.Button(self, text="Back",
                           command=lambda: self.controller.show_frame(MuseumReviews))
        self.b.grid(row=ind, column=150)


class AllMuseums(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Museums").grid(row=0, column=150)
        tk.Label(self, text="Rating").grid(row=0, column=300)

        museums = db.getallmuseums()
        ind = 0;
        mList = [];
        rList = [];
        for m in museums:
            museum = m['museum_name']
            if (museum != ""''""):
                mList.insert(ind, museum)
            ind = ind + 1
        ind = 0
        for r in museums:
            rating = r['avg(review.rating)']
            if (museum != ""''""):
                rList.insert(ind, rating)
            ind = ind + 1
        ind = 1
        self.LabelList = []
        labInd = 0
        for mus in mList:
            self.l = tk.Label(self, text=mus)
            self.l.grid(row=ind, column=150)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for r in rList:
            if r != None:
                self.l = tk.Label(self, text=str(round(r, 2)) + "/5")
            else:
                self.l = tk.Label(self, text="--/5")
            self.l.grid(row=ind, column=300)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        self.con = controller
        self.b = tk.Button(self, text="Back",
                           command=lambda: self.properHomeScreen(controller))
        self.b.grid(row=ind, column=0)

    def update(self):
        for l in self.LabelList:
            l.grid_forget()

        self.b.grid_forget()
        museums = db.getallmuseums()
        ind = 0;
        mList = [];
        rList = [];
        for m in museums:
            museum = m['museum_name']
            if (museum != ""''""):
                mList.insert(ind, museum)
            ind = ind + 1
        ind = 0
        for r in museums:
            rating = r['avg(review.rating)']
            if (museum != ""''""):
                rList.insert(ind, rating)
            ind = ind + 1
        ind = 1
        self.LabelList = []
        labInd = 0
        for mus in mList:
            self.l = tk.Label(self, text=mus)
            self.l.grid(row=ind, column=150)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for r in rList:
            if r != None:
                self.l = tk.Label(self, text=str(round(r, 2)) + "/5")
            else:
                self.l = tk.Label(self, text="--/5")
            self.l.grid(row=ind, column=300)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1

        self.b = tk.Button(self, text="Back",
                           command=lambda: self.properHomeScreen(self.con))
        self.b.grid(row=ind, column=0)

    def properHomeScreen(self, controller):
        global isCurator
        if(isCurator):
            controller.show_frame(CuratorHomePage)
        else:
            controller.show_frame(HomePage)

class MyTickets(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="My Tickets").grid(row=0, column=300)
        tk.Label(self, text="Museum").grid(row=1, column=201)
        tk.Label(self, text="Purchase Date").grid(row=1, column=300)
        tk.Label(self, text="Price").grid(row=1, column=450)
        global user
        tickets = db.viewmytickets(user)
        ind = 0;
        tList = [];
        pdList = [];
        pList = [];
        for t in tickets:
            museum = t['museum_name']
            if (museum != ""''""):
                tList.insert(ind, museum)
            ind = ind + 1
        ind = 0
        for pd in tickets:
            date = pd['purchase_timestamp']
            if (date != ""''""):
                pdList.insert(ind, date)
            ind = ind + 1
        ind = 0
        for pd in tickets:
            date = pd['price']
            if (date != ""''""):
                pList.insert(ind, date)
            ind = ind + 1

        ind = 1

        self.LabelList = []
        labInd = 0
        for m in tList:
            self.l = tk.Label(self, text=m)
            self.l.grid(row=200 + ind, column=201)
            self.LabelList.insert(labInd, self.l)
            ind = ind + 1
            labInd = labInd + 1

        ind = 1
        for d in pdList:
            self.l = tk.Label(self, text=d)
            self.l.grid(row=200 + ind, column=300)
            self.LabelList.insert(labInd, self.l)
            ind = ind + 1
            labInd = labInd + 1
        ind = 1
        for p in pList:
            self.l = tk.Label(self, text=p)
            self.l.grid(row=200 + ind, column=450)
            self.LabelList.insert(labInd, self.l)
            ind = ind + 1
            labInd = labInd + 1
        self.con = controller;
        self.b = tk.Button(self, text="Back",
                           command=lambda: self.properHomeScreen(self.con))
        self.b.grid(row=200 + ind, column=300)

    def update(self):
        for l in self.LabelList:
            l.grid_forget()
        self.b.grid_forget()
        global user
        tickets = db.viewmytickets(user)
        ind = 0;
        tList = [];
        pdList = [];
        pList = [];
        for t in tickets:
            museum = t['museum_name']
            if (museum != ""''""):
                tList.insert(ind, museum)
            ind = ind + 1
        ind = 0
        for pd in tickets:
            date = pd['purchase_timestamp']
            if (date != ""''""):
                pdList.insert(ind, date)
            ind = ind + 1
        ind = 0
        for pd in tickets:
            date = pd['price']
            if (date != ""''""):
                pList.insert(ind, date)
            ind = ind + 1

        ind = 1

        self.LabelList = []
        labInd = 0
        for m in tList:
            self.l = tk.Label(self, text=m)
            self.l.grid(row=200 + ind, column=201)
            self.LabelList.insert(labInd, self.l)
            ind = ind + 1
            labInd = labInd + 1

        ind = 1
        for d in pdList:
            self.l = tk.Label(self, text=d)
            self.l.grid(row=200 + ind, column=300)
            self.LabelList.insert(labInd, self.l)
            ind = ind + 1
            labInd = labInd + 1
        ind = 1
        for p in pList:
            self.l = tk.Label(self, text=p)
            self.l.grid(row=200 + ind, column=450)
            self.LabelList.insert(labInd, self.l)
            ind = ind + 1
            labInd = labInd + 1
        self.b = tk.Button(self, text="Back",
                           command=lambda: self.properHomeScreen(self.con))
        self.b.grid(row=200 + ind, column=300)
        
    def properHomeScreen(self, controller):
        global isCurator
        if(isCurator):
            controller.show_frame(CuratorHomePage)
        else:
            controller.show_frame(HomePage)

class MyReviews(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="My Reviews").grid(row=0, column=300)
        tk.Label(self, text="Museum").grid(row=1, column=201)
        tk.Label(self, text="Comment").grid(row=1, column=300)
        tk.Label(self, text="Rating").grid(row=1, column=450)
        global user
        reviews = db.viewmyreviews(user)
        ind = 0;
        mList = [];
        cList = [];
        rList = [];
        for m in reviews:
            museum = m['museum_name']
            if (museum != ""''""):
                mList.insert(ind, museum)
            ind = ind + 1
        ind = 0
        for c in reviews:
            comment = c['comment']
            if (comment != ""''""):
                cList.insert(ind, comment)
            ind = ind + 1
        ind = 0
        for r in reviews:
            rate = r['rating']
            rList.insert(ind, rate)
            ind = ind + 1
        self.LabelList = []
        labInd = 0
        ind = 1
        for m in mList:
            self.l = tk.Label(self, text=m)
            self.l.grid(row=2 + ind, column=201)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for d in cList:
            self.l = tk.Label(self, text=d)
            self.l.grid(row=2 + ind, column=300)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for p in rList:
            self.l = tk.Label(self, text=p)
            self.l.grid(row=2 + ind, column=450)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        self.con = controller
        self.b = tk.Button(self, text="Back",
                           command=lambda: self.properHomeScreen(controller))
        self.b.grid(row=200 + ind, column=300)

    def properHomeScreen(self, controller):
        global isCurator
        if(isCurator):
            controller.show_frame(CuratorHomePage)
        else:
            controller.show_frame(HomePage)

    def update(self):
        for l in self.LabelList:
            l.grid_forget()
        self.b.grid_forget()

        global user
        reviews = db.viewmyreviews(user)
        ind = 0;
        mList = [];
        cList = [];
        rList = [];
        for m in reviews:
            museum = m['museum_name']
            if (museum != ""''""):
                mList.insert(ind, museum)
            ind = ind + 1
        ind = 0
        for c in reviews:
            comment = c['comment']
            if (comment != ""''""):
                cList.insert(ind, comment)
            ind = ind + 1
        ind = 0
        for r in reviews:
            rate = r['rating']
            rList.insert(ind, rate)
            ind = ind + 1
        self.LabelList = []
        labInd = 0
        ind = 1
        for m in mList:
            self.l = tk.Label(self, text=m)
            self.l.grid(row=2 + ind, column=201)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for d in cList:
            self.l = tk.Label(self, text=d)
            self.l.grid(row=2 + ind, column=300)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for p in rList:
            self.l = tk.Label(self, text=p)
            self.l.grid(row=2 + ind, column=450)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        self.b = tk.Button(self, text="Back",
                           command=lambda: self.properHomeScreen(self.con))
        self.b.grid(row=200 + ind, column=300)
    


class ManageAccount(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Manage Account").grid(row=0, column=150)
        global user
        button1 = tk.Button(self, text="Log Out",
                            command=lambda: controller.show_frame(LoginPage)).grid(row=400, column=150)

        button2 = tk.Button(self, text="Curator Request",
                            command=lambda: controller.show_frame(CreateCuratorRequest)).grid(row=401, column=150)
        button3 = tk.Button(self, text="Delete Account",
                            command=lambda: self.deleteA(controller)).grid(row=402, column=150)
        b = tk.Button(self, text="Back",
                      command=lambda: self.properHomeScreen(controller)).grid(row=403, column=2)

    def properHomeScreen(self, controller):
        global isCurator
        if(isCurator):
            controller.show_frame(CuratorHomePage)
        else:
            controller.show_frame(HomePage)
            
    def deleteA(self, controller):
        delPop = tk.Tk()
        delPop.geometry("400x300")
        delPop.wm_title("Are you Sure?")
        tk.Label(delPop, text="Deleting Account will remove all personal data and reviews.").grid(row=0, column=0)
        tk.Button(delPop, text="Yes", command=lambda: self.deleteSelected(controller, delPop)).grid(row=1, column=0)
        tk.Button(delPop, text="No, Don't!", command=delPop.destroy).grid(row=2, column=0)
        delPop.mainloop()

    def deleteSelected(self, controller, root):
        global user
        root.destroy()
        db.deleteaccount(user)
        controller.show_frame(LoginPage)


class CreateCuratorRequest(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Create Curator Request").grid(row=0, column=150)
        global user

        museums = db.allmuseums()
        ind = 0;
        Mlist = [];
        self.var = tk.StringVar()
        self.var.set('Museums')
        for m in museums:
            museum = m['museum_name']
            if (museum != ""''""):
                Mlist.insert(ind, museum)
            ind = ind + 1
        self.l2 = tk.Label(self, text="Choose a Museum:")
        self.l2.grid(row=399, column=0)
        self.o = tk.OptionMenu(self, self.var, *Mlist, command=print(self.var.get()))
        self.o.grid(row=399, column=150)
        response = tk.Button(self, text="Submit", command=lambda: self.createReq(user, self.var.get())).grid(row=400,
                                                                                                             column=150)
        b = tk.Button(self, text="Back",
                      command=lambda: controller.show_frame(HomePage)).grid(row=403, column=0)

    def createReq(self, euser, mus):
        response = db.createcuratorreq(euser, mus)
        if (response == 2):
            popupBox("Error", "Museum already has a curator")
        elif (response == 5):
            popupBox("Error", "You've already made the request!")
        else:
            popupBox("Success", "Curator Request Submitted")

    def update(self):
        self.o.grid_forget()
        museums = db.allmuseums()
        ind = 0;
        Mlist = [];
        for m in museums:
            museum = m['museum_name']
            if (museum != ""''""):
                Mlist.insert(ind, museum)
            ind = ind + 1
        self.var.set("Museum")
        self.o = tk.OptionMenu(self, self.var, *Mlist, command=print(self.var.get()))
        self.o.grid(row=399, column=150)


class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Welcome Admin").grid(row=0, column=2)
        global user
        button1 = tk.Button(self, text="Accept Curator Requests",
                            command=lambda: controller.show_frame(AcceptCurators)).grid(row=400, column=2)

        button2 = tk.Button(self, text="Add Museum",
                            command=lambda: controller.show_frame(AddMuseums)).grid(row=401, column=2)
        button3 = tk.Button(self, text="Delete Museum",
                            command=lambda: controller.show_frame(DeleteMuseums)).grid(row=402, column=2)
        button4 = tk.Button(self, text="Log Out",
                            command=lambda: controller.show_frame(LoginPage)).grid(row=403, column=2)


class AcceptCurators(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Accept Curators").grid(row=0, column=150)
        tk.Label(self, text="Museum").grid(row=0, column=300)
        tk.Label(self, text="Curator Email").grid(row = 0,column = 450)

        requests = db.getallcuratorrequests()
        ind = 0
        mList = []
        rList =[]
        mDict = {}
        cDict = {}
        for m in requests:
            museum = m['museum_name']
            if (museum != ""''""):
                mList.insert(ind, museum)
                mDict[ind + 1] = museum
            ind = ind + 1
        ind = 0
        for r in requests:
            cemail = r['email']
            if (museum != ""''""):
                rList.insert(ind, cemail)
                cDict[ind + 1] = cemail
            ind = ind + 1
        ind = 1
        LabInd = 0
        self.LabelList = []
        for mus in mList:
            self.l = tk.Label(self, text=mus)
            self.l.grid(row=ind, column = 300)
            self.LabelList.insert(LabInd, self.l)
            ind = ind + 1
            LabInd += 1
        ind = 1
        for r in rList:
            self.l = tk.Label(self, text= r)
            self.l.grid(row=ind, column = 450)
            self.LabelList.insert(LabInd, self.l)
            #Not perfect. Need way to store museum name and curator email.
            ind = ind + 1
            LabInd += 1
        self.ButtonList=[]
        for x in range(0, len(mList)):
            self.AcceptButton = tk.Button(self,text = "Accept",
                                     command = lambda x = x:  db.acceptcuratorrequest(user, cDict[x + 1], mDict[x + 1]))
            self.AcceptButton.grid(row = x+1, column = 550)
            self.ButtonList.append(self.AcceptButton)
            self.DeclineButton = tk.Button(self, text = "Decline",
                                      command = lambda x = x: db.deletecuratorrequest(user, cDict[x + 1], mDict[x + 1]))
            self.DeclineButton.grid(row = x+1, column = 600)
            self.ButtonList.append(self.DeclineButton)
            x += 1
        self.con = controller
        self.button4 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(AdminPage))
        self.button4.grid(row=403, column=150)

    def update(self):
        for l in self.LabelList:
            l.grid_forget()
        self.button4.grid_forget()
        for b in self.ButtonList:
            b.grid_forget()
        

        requests = db.getallcuratorrequests()
        ind = 0
        mList = []
        rList =[]
        mDict = {}
        cDict = {}
        for m in requests:
            museum = m['museum_name']
            if (museum != ""''""):
                mList.insert(ind, museum)
                mDict[ind + 1] = museum
            ind = ind + 1
        ind = 0
        for r in requests:
            cemail = r['email']
            if (museum != ""''""):
                rList.insert(ind, cemail)
                cDict[ind + 1] = cemail
            ind = ind + 1
        ind = 1
        LabInd = 0
        self.LabelList = []
        for mus in mList:
            self.l = tk.Label(self, text=mus)
            self.l.grid(row=ind, column = 300)
            self.LabelList.insert(LabInd, self.l)
            ind = ind + 1
            LabInd += 1
        ind = 1
        for r in rList:
            self.l = tk.Label(self, text= r)
            self.l.grid(row=ind, column = 450)
            self.LabelList.insert(LabInd, self.l)
            #Not perfect. Need way to store museum name and curator email.
            ind = ind + 1
            LabInd += 1
        self.ButtonList = []
        for x in range(0, len(mList)):
            self.AcceptButton = tk.Button(self,text = "Accept",
                                     command = lambda x = x:  self.accept(user, cDict[x + 1], mDict[x + 1]))
            self.AcceptButton.grid(row = x+1, column = 550)
            self.ButtonList.append(self.AcceptButton)
            self.DeclineButton = tk.Button(self, text = "Decline",
                                      command = lambda x = x: self.remove(user, cDict[x + 1], mDict[x + 1]))
            self.DeclineButton.grid(row = x+1, column = 600)
            self.ButtonList.append(self.DeclineButton)
            x += 1
        self.button4 = tk.Button(self, text="Back",
                            command=lambda: self.con.show_frame(AdminPage))
        self.button4.grid(row=403, column=150)

    def remove(self, user, email, museum):
        db.deletecuratorrequest(user, email, museum)
        self.update()
    def accept(self, user, email, museum):
        db.acceptcuratorrequest(user, email, museum)
        self.update()


class AddMuseums(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Add Museums").grid(row=0, column=150)
        tk.Label(self, text="Name of New Museum:").grid(row=1, column=149)
        self.e1 = tk.Entry(self)
        self.e1.grid(row=1, column=150)
        b = tk.Button(self, text="Submit Museum",
                      command=lambda: self.addMuseum(controller)).grid(row=403, column=150)
        button4 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(AdminPage)).grid(row=404, column=150)

    def addMuseum(self, controller):
        check = db.addmuseum(self.e1.get())
        if (check == 1):
            popupBox("Success", "Museum Successfully Added")
        elif (check == 2):
            popupBox("Error", "Museum Already Exists")
        self.e1.delete(0, 'end')


class DeleteMuseums(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Delete Museums").grid(row=0, column=150)
        self.var = tk.StringVar()
        self.var.set('Museums')
        self.dropMenu = self.getmlist()
        tk.Label(self, text="Choose a Museum:").grid(row=399, column=0)
        self.o = tk.OptionMenu(self, self.var, *self.dropMenu, command=print(self.var.set(self.var.get())))
        self.o.grid(row=399, column=150)
        tk.Button(self, text="Delete Museum",
                  command=lambda: self.var.set(self.removeMuseum(controller, self.var.get()))).grid(row=400, column=150)
        button4 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(AdminPage)).grid(row=403, column=150)

    def removeMuseum(self, controller, museumName):
        int1 = db.deletemuseum(museumName)
        if (int1 == 0):
            popupBox("Error", "Museum does not exist in Database")
        else:
            self.update()

    def getmlist(self):
        museums = db.allmuseums()
        ind = 0;
        Mlist = [];

        for m in museums:
            museum = m['museum_name']
            if (museum != ""''""):
                Mlist.insert(ind, museum)
            ind = ind + 1
        return Mlist

    def update(self):
        self.o.grid_forget()
        self.dropMenu = self.getmlist()
        self.var.set('Museums')
        self.o = tk.OptionMenu(self, self.var, *self.dropMenu, command=print(self.var.get()))
        self.o.grid(row=399, column=150)


class CuratorMuseums(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Museums").grid(row=0, column=150)
        tk.Label(self, text="Rating").grid(row=0, column=300)
        tk.Label(self, text="Count").grid(row=0, column=450)
        self.firstRun = True
        self.con = controller



    def update(self):
        if (self.firstRun == False):
            for l in self.LabelList:
                l.grid_forget()

            self.b.grid_forget()

        global user

        museums = db.mycuratormuseums(user)
        ind = 0
        mList = []
        rList = []
        cList = []
        for m in museums:
            museum = m['museum_name']
            mList.insert(ind, museum)
            ind = ind + 1
        ind = 0
        for r in museums:
            rating = r['AVG(r.rating)']
            rList.insert(ind, rating)
            ind = ind + 1
        ind = 0
        for c in museums:
            count = c['COUNT(DISTINCT e.exhibit_name)']
            cList.insert(ind, count)
            ind += 1
        ind = 1
        self.LabelList = []
        labInd = 0
        for mus in mList:
            self.l = tk.Label(self, text=mus)
            self.l.grid(row=ind, column=150)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for r in rList:
            if r != None:
                self.l = tk.Label(self, text=str(round(r, 2)) + "/5")
            else:
                self.l = tk.Label(self, text="--/5")
            self.l.grid(row=ind, column=300)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for c in cList:
            if c != None:
                self.l = tk.Label(self, text=c)
            else:
                self.l = tk.Label(self, text="0")
            self.l.grid(row=ind, column=450)
            self.LabelList.insert(labInd, self.l)
            labInd += 1
            ind += 1

        self.b = tk.Button(self, text="Back",
                           command=lambda: self.properHomeScreen(self.con))
        self.b.grid(row=ind, column=0)
        self.firstRun = False

    def properHomeScreen(self, controller):
        global isCurator
        if(isCurator):
            controller.show_frame(CuratorHomePage)
        else:
            controller.show_frame(HomePage)

class AddExhibit(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Add a New Exhibit").grid(row=0, column=150)
        tk.Label(self, text="Name of New Exhibit:").grid(row=2, column=149)
        tk.Label(self, text="Year:").grid(row=3, column=149)
        tk.Label(self, text="Link to More info:").grid(row=4, column=149)
        self.e1 = tk.Entry(self)
        self.e2 = tk.Entry(self)
        self.e3 = tk.Entry(self)
        self.e1.grid(row=2, column=150)
        self.e2.grid(row=3, column=150)
        self.e3.grid(row=4, column=150)
        self.controller = controller

        self.b = tk.Button(self, text="Submit Exhibit",
                           command=lambda: self.addExhibit()).grid(row=403, column=150)

        button4 = tk.Button(self, text="Back", command=lambda: controller.show_frame(CuratorSpecificMuseums)).grid(row=404,
                                                                                                          column=150)

    def addExhibit(self):
        global mName
        global user
        check = db.addexhibit(mName, self.e1.get(), self.e2.get(), self.e3.get(), user)
        self.e1.delete(0, 'end')
        self.e2.delete(0, 'end')
        self.e3.delete(0, 'end')
        if (check == 1):
            popupBox("Success", "Exhibit Successfully Added")

        elif (check == 2):
            popupBox("Error", "Exhibit Already Exists")
        elif (check ==3):
            popupBox("Error",  "You are not a curator for this museum")

class CuratorSpecificMuseums(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global mName
        self.controller = controller
        self.l1 = tk.Label(self, text="Welcome to the: " + mName + "!")
        self.l1.grid(row=0, column=300)
        tk.Label(self, text="Exhibit").grid(row=1, column=201)
        tk.Label(self, text="Year").grid(row=1, column=300)
        tk.Label(self, text="Url").grid(row=1, column=450)
        tk.Label(self, text="Delete Exhibit").grid(row=1, column=651)
        exhibits = db.viewspecificmuseum(mName)
        ind = 0;
        eList = []
        yList = []
        uList = []
        eDict = {}
        for e in exhibits:
            exhibit = e['exhibit_name']
            if (exhibit != ""''""):
                eList.insert(ind, exhibit)
                eDict[ind + 1] = museum
            ind = ind + 1
        ind = 0
        for y in exhibits:
            year = y['year']
            yList.insert(ind, year)
            ind = ind + 1
        ind = 0
        for u in exhibits:
            url = u['url']
            uList.insert(ind, url)
            ind = ind + 1

        ind = 1

        self.LabelList = []
        labInd = 0
        for m in eList:
            self.l = tk.Label(self, text=m)
            self.l.grid(row=2 + ind, column=201)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for d in yList:
            self.l = tk.Label(self, text=d)
            self.l.grid(row=2 + ind, column=300)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for p in uList:
            self.l = tk.Label(self, text=p)
            self.l.grid(row=2 + ind, column=450)
            self.LabelList.insert(labInd, self.l)
            labInd = labInd + 1
            ind = ind + 1
        self.bList = []
        for x in range(0, len(eList)):
            self.DeleteButton = tk.Button(self, text="Delete Exhibit",
                                     command=lambda x=x: self.removeExhibit(mName, eDict[x + 1]))
            self.DeleteButton.grid(row=x + 1, column=651)
            self.bList.append(self.DeleteButton)

        tk.Button(self, text="Purchase Ticket",
                  command=lambda: self.purchaseTicket()).grid(row=300 + ind, column=300)
        tk.Button(self, text="Review Museum",
                  command=lambda: controller.show_frame(ReviewMuseum)).grid(row=301 + ind, column=300)
        tk.Button(self, text="View Other Reviews",
                  command=lambda: controller.show_frame(SpecificMAllReviews)).grid(row=302 + ind, column=300)
        self.b = tk.Button(self, text="Add Exhibit",
                           command=lambda: self.controller.show_frame(AddExhibit))
        self.b.grid(row=303 + ind, column=300)
        tk.Button(self, text="Back",
                  command=lambda: self.properHomeScreen(controller)).grid(row=350 + ind, column=0)

    def properHomeScreen(self, controller):
        global isCurator
        if(isCurator):
            controller.show_frame(CuratorHomePage)
        else:
            controller.show_frame(HomePage)
    def removeExhibit(self, museum, exhibit):
        global user
        result = db.removeexhibit(museum, exhibit, user)
        self.update()
        if (result == 3):
            popupBox("Error", "You are not a curator for this museum")
        
        

    def purchaseTicket(self):
        check = db.purchaseticket(user, mName)
        if (check == 1):
            popupBox("Success", "Thank You for Purchasing a Ticket to the " + mName)
        elif (check == 4):
            popupBox("Error", "You already bought a ticket to " + mName)

    def update(self):
        global mName

        self.l1.grid_forget()
        self.l1 = tk.Label(self, text="Welcome to the: " + mName + "!")
        self.l1.grid(row=0, column=300)

        for l in self.LabelList:
            l.grid_forget()

        for b in self.bList:
            b.grid_forget()

        exhibits = db.viewspecificmuseum(mName)
        ind = 0;
        eList = [];
        yList = [];
        uList = [];
        eDict = {}
        for e in exhibits:
            exhibit = e['exhibit_name']
            if (exhibit != ""''""):
                eList.insert(ind, exhibit)
                eDict[ind + 1] = exhibit
            ind = ind + 1
        ind = 0
        for y in exhibits:
            year = y['year']
            yList.insert(ind, year)
            ind = ind + 1
        ind = 0
        for u in exhibits:
            url = u['url']
            uList.insert(ind, url)
            ind = ind + 1

        ind = 1

        self.LabelList = []
        labInd = 0
        for m in eList:
            self.l = tk.Label(self, text=m)
            self.l.grid(row=2 + ind, column=201)
            self.LabelList.append(self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for d in yList:
            self.l = tk.Label(self, text=d)
            self.l.grid(row=2 + ind, column=300)
            self.LabelList.append(self.l)
            labInd = labInd + 1
            ind = ind + 1
        ind = 1
        for p in uList:
            self.l = tk.Label(self, text=p)
            self.l.grid(row=2 + ind, column=450)
            self.LabelList.append(self.l)
            labInd = labInd + 1
            ind = ind + 1
        self.bList = []
        for x in range(0, len(eList)):
            self.DeleteButton = tk.Button(self, text="Delete Exhibit",
                                          command=lambda x=x: self.removeExhibit(mName, eDict[x + 1]))
            self.DeleteButton.grid(row=x + 3, column=651)
            self.bList.append(self.DeleteButton)

app = GUI()
app.wm_title("BMTRS")
app.geometry("600x600")  # set Gui size
app.resizable(0, 0)
app.mainloop()
