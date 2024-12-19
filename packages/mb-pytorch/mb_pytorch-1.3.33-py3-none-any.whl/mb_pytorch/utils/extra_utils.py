from torchsummary import summary
import onnx
from onnx2pytorch import ConvertModel
import torch
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mb_pandas.dfload import load_any_df
import pandas as pd

__all__ = ['get_model_summary','onnx2torch','overwrite_layer_weights','feature_extractor','feature_view','labels_num_map']


def get_model_summary(model, input_size):
    """Prints the model summary.
    Input:
        model: PyTorch model
        input_size: input size of the model
    """
    summary(model, input_size=input_size)
    
def onnx2torch(model):
    """
    Function to convert onnx model to torch model
    Input:
        model: onnx model
    Output:
        torch model
    """
    onnx_m = onnx.load(model)
    torch_m = ConvertModel(onnx_m)
    return torch_m


def overwrite_layer_weights(model, layer_index, new_weights,logger=None):
    """
    Overwrites the weights of a specified layer of a PyTorch model with the given weights.
    Args:
    - model: A PyTorch model.
    - layer_index: The index of the layer whose weights should be overwritten.
    - new_weights: A tensor containing the new weights to be used for the specified layer.
    """

    layer_name = list(model.named_modules())[layer_index][0]
    layer = getattr(model, layer_name)
    if logger:
        logger.info("Overwriting the weights of layer {} with the given weights.".format(layer_name))
    if isinstance(layer, torch.nn.Conv2d):
        layer.weight.data = new_weights
    if isinstance(layer, torch.nn.Linear):
        layer.weight.data = new_weights
    else:
        raise ValueError("The specified layer is not a convolutional layer or linear layer.")

def labels_num_map(input_csv, output_csv=None,is_train=True):
    if isinstance(input_csv, str):
        df = load_any_df(input_csv)
    else:
        df = input_csv

    if is_train:
        # print(f'dataframe1: {df.head()}')
        labels_list = df['label'].to_list()
        labels_list2 = [[i] for i in labels_list if isinstance(i, str)]
        unique_labels = list(set([label for labels in labels_list2 for label in labels]))
        label_num_map = {label: i for i, label in enumerate(unique_labels)}

        # print(f'label map :{label_num_map}')
        new_pd = pd.DataFrame(columns=['label', 'label_num'])
        new_pd['label'] = list(label_num_map.keys())
        new_pd['label_num'] = list(label_num_map.values())
        if output_csv:
            new_pd.to_csv(output_csv, index=False)
    else:
        new_pd = load_any_df(output_csv)
        labels_list = df['label'].to_list()
        labels_list2 = [[i] for i in labels_list if isinstance(i, str)]
        label_num_map = dict(zip(new_pd['label'], new_pd['label_num']))

    labels_num =[]
    for i in labels_list2:
        temp_list = []
        for j in range(len(i)):
            temp_list.append(label_num_map[i[j]])
        labels_num.append(temp_list)
        labels_final_num = [xs[x] for xs in labels_num for x in range(len(xs))]
    # print(f'dataframe2: {df.head()}')
    # print(f'labels_final_num: {labels_final_num}')
    df['label_num'] = labels_final_num
    return df


def feature_extractor(model, layer_name):
    """
    Function to get the feature extractor from the model.
    Args:
        model (torch.nn.Module): PyTorch model
        layer_name (str): Name of the layer to be used as feature extractor
    Returns:
        feature_extractor (torch.nn.Sequential): Feature extractor from the model
    """
    # Get the named module from the model
    module = dict(model.named_modules())[layer_name]
    # Get the position of the named module in the list of all modules
    layer_loc = list(model.modules()).index(module)
    # Extract the feature extractor from the model
    feature_extractor = torch.nn.Sequential(*list(model.children())[:layer_loc])
    return feature_extractor


def feature_view(data,model,layer_names:list) -> None:
    """
    Function to view image from the feature extractor
        data: Image data
        model: PyTorch model
        layer_names (list): Name of the layer to be used as feature extractor
    Output:
        feature_view: Feature view from the model
    """
    out_list = []
    for j in data:
        for i in range(len(layer_names)):
            layer = layer_names[i]
            features = feature_extractor(model,layer)
            #features = getattr(model,layer)
            output = features(j)
            output = output.squeeze(0).detach().numpy()
            out_list.append(output)
        fig, axs = plt.subplots(1, len(layer_names), figsize=(12, 12))
        for i in range(len(layer_names)):
            if len(out_list[i].shape) > 2:
                out_map = np.sum(out_list[i], axis=0)
            else:
                out_map = out_list[i]
            sns.heatmap(out_map, ax=axs[i])
            axs[i].set_title(f'{layer_names[i]} : {out_list[i].shape}' )
    return None
        