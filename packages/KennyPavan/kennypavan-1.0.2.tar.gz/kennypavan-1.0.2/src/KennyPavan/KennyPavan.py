class KennyPavan:
	def __init__(self):
		self.name = "Kenny Pavan"
		self.email = "kennypavan@protonmail.com"
		self.github = "https://github.com/kennypavan/"
		self.linkedin = "https://www.linkedin.com/in/kennypavan/"
		self.website = "https://www.kennypavan.com/"
		self.bluesky = "https://bsky.app/profile/kennypavan.com"
		self.instagram = "https://www.instagram.com/kennypavan/"

	def displayAll(self):
		print("\n")
		print(self.name)
		print(self.email)
		print("Website: " + self.website)
		print("Github: " + self.github)
		print("LinkedIn: " + self.linkedin)
		print("Bluesky: " + self.bluesky)
		print("Instagram: " + self.instagram)
		print("\n")
		self.about()
		print("\n")
		self.education()
		print("\n")
		self.skills()
		print("\n")
		self.experience()
		print("\n")
		self.publications()
		print("\n")

	def about(self):
		output = "\nAbout\n\n"
		output += "Experienced Software Developer with a demonstrated history of working in the computer software industry. Skilled in Python, Java, C++, Javascript, PHP (Laravel), Linux, SQL, and Computational Biology. Strong engineering professional with multiple bachelor degrees. Currently leveraging machine learning, graph convolutional neural networks, and various computational strategies to unravel complex biological systems, particularly in single cell and spatial analyses.\n"
		print(output)

	def education(self):
		output = "Education\n\n"
		output += "\tPhD. Biomedical Engineering, Oregon Health and Science University (expected 2026)\n"
		output += "\tB.S. Computer Science, Western Governors University\n"
		output += "\tB.S. Molecular Biology, Montclair State University\n"
		output += "\tB.A. Digital Communication and Media/Multimedia, Ramapo College\n"
		print(output)

	def skills(self):
		output = "Skills\n\n"
		output += "\tPython\n"
		output += "\tJavaScript\n"
		output += "\tC++\n"
		output += "\tJava\n"
		output += "\tPHP (Laravel)\n"
		output += "\tHTML/CSS\n"
		output += "\tSQL (various flavors)\n"
		output += "\tMachine learning\n"
		output += "\tData visualization\n"
		output += "\tWeb development\n"
		output += "\tBioinformatics\n"
		output += "\tSingle-cell Analysis\n"
		output += "\tSpatial Analysis\n"
		output += "\tPlatform Development\n"
		print(output)

	def experience(self):
		output = "Experience\n\n"
		output += "\tOregon Health & Science University\n"
		output += "\t\tBiomedical Engineering PhD Candidate: Developing high-throughput analysis packages to understand synaptic connectivity.\n\n"
		output += "\taDNATool\n"
		output += "\t\tFounder & Bioinformatics Developer: Built an elastic platform for RNA-Seq analysis (2021-2022).\n\n"
		output += "\tSelf-Employed (Software Development)\n"
		output += "\t\tFull-Stack Engineer & Consultant: Developed cloud-based inventory and blockchain projects (2019-2022).\n\n"
		output += "\tAnchor Digital, Inc.\n"
		output += "\t\tSenior Database & Backend Developer: Built an institutional trading platform using blockchain (2017-2020).\n\n"
		output += "\tXY Group, LLC\n"
		output += "\t\tFounder & Lead Developer: Managed a team of six to deliver eCommerce platforms, iOS apps, and operational tools (2009-2015).\n"
		print(output)

	def publications(self):
		output = "Publications\n\n"
		output += "\tAnnSQL: A Scalable SQL Interface for Single-Cell Data\n"
		output += "\t\tAuthors: Kenny Pavan, Arpiar Saunders.\n"
		output += "\t\tDOI: https://doi.org/10.1101/2024.11.02.621676\n"
		output += "\t\tThe tool streamlines single-cell data processing and supports efficient SQL querying of large-scale datasets."
		print(output)
