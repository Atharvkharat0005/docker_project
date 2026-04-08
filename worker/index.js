
const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());


const MONGO_URI = process.env.MONGO_URI || 
"mongodb+srv://atharvkharat68_db_user:hvccPYMgLuo8l6H5@cluster0.dbpu8k9.mongodb.net/socialdb?retryWrites=true&w=majority";


mongoose.connect(MONGO_URI)
.then(() => console.log("✅ MongoDB Connected"))
.catch(err => console.error("❌ MongoDB Error:", err));


const postSchema = new mongoose.Schema({}, { strict: false });
const Post = mongoose.model("Post", postSchema, "posts");


app.get("/posts", async (req, res) => {
    try {
        const posts = await Post.find().sort({ _id: -1 });
        res.json(posts);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});


app.post("/posts", async (req, res) => {
    try {
        const { platform, content } = req.body;


        if (!platform || typeof platform !== "string") {
            return res.status(400).json({
                error: "Platform must be a string"
            });
        }

        if (!content || typeof content !== "string") {
            return res.status(400).json({
                error: "Content must be a string"
            });
        }

        const newPost = new Post({
            platform,
            content,
            sent: false  
        });

        const savedPost = await newPost.save();

        res.status(201).json({
            message: "Post added successfully",
            data: savedPost
        });

    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});


app.get("/", (req, res) => {
    res.send("Server is running 🚀");
});


const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});