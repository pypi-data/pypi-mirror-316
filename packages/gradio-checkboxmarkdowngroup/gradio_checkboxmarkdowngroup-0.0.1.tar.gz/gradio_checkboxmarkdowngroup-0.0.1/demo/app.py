from typing import List
import gradio as gr

from gradio_checkboxmarkdowngroup.checkboxmarkdowngroup import Choice
from gradio_checkboxmarkdowngroup import CheckboxMarkdownGroup


choices = [
    Choice(id="art_101", title="Understanding Neural Networks", content="# Understanding Neural Networks\nThis article explains the basics of neural networks, their architecture, and how they learn from data."),
    Choice(id="art_102", title="A Gentle Introduction to Transformers", content="# A Gentle Introduction to Transformers\nTransformers have revolutionized NLP. Learn about attention mechanisms, encoder-decoder architecture, and the future of large language models."),
    Choice(id="art_103", title="Reinforcement Learning Basics", content="# Reinforcement Learning Basics\nAn overview of RL concepts like agents, environments, rewards, and how RL differs from supervised and unsupervised learning."),
    Choice(id="art_104", title="Generative Adversarial Networks (GANs)", content="# Generative Adversarial Networks (GANs)\nDiscover how GANs pair a generator and discriminator to create realistic images, text, and other synthetic data."),
    Choice(id="art_105", title="Convolutional Neural Networks (CNNs)", content="# Convolutional Neural Networks (CNNs)\nLearn about convolution, pooling, and how CNNs excel at image recognition tasks."),
    Choice(id="art_106", title="Graph Neural Networks", content="# Graph Neural Networks\nAn intro to applying neural networks to graph-structured data, covering message passing and graph embeddings."),
]


def sentence_builder(selected):
    if not selected:
        return "You haven't selected any articles yet."
    
    if isinstance(selected[0], dict) and "title" in selected[0]:
        formatted_choices = []
        for choice in selected:
            formatted_choices.append(
                f"ID: {choice['id']}\nTitle: {choice['title']}\nContent: {choice['content']}"
            )
        return "Selected articles are:\n\n" + "\n\n".join(formatted_choices)
    else:
        return (
            "Selected articles are :\n\n- "
            + "\n- ".join(selected)
        )

with gr.Blocks() as demo:
    
    with gr.Row():
    
        checkbox_group = CheckboxMarkdownGroup(
            choices=choices,
            label="Select Articles",
            info="Choose articles to include in your collection",
            type="all"
        )
        
        output_text = gr.Textbox(
            label="Selected Articles",
            placeholder="Make selections to see results...",
            info="Selected articles will be displayed here",
        )
            
    checkbox_group.change(
        fn=sentence_builder,
        inputs=checkbox_group,
        outputs=output_text
    )

if __name__ == '__main__':
    demo.launch()
