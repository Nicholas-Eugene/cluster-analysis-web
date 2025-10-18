"""
PDF Generator for clustering results with visualizations
"""

from io import BytesIO
import matplotlib

# Force Agg backend before importing pyplot
matplotlib.use("Agg", force=True)
# Clear any existing figures
matplotlib.pyplot.close("all")
import matplotlib.pyplot as plt
import seaborn as sns

# Configure plot style with a built-in style
plt.style.use("default")  # Use default style as base
sns.set(style="whitegrid", font_scale=1.2)  # Set seaborn defaults
sns.set_palette("husl")  # Use a color-blind friendly palette

# Set default figure settings
plt.rcParams.update(
    {
        "figure.figsize": (10, 6),
        "figure.dpi": 300,
        "figure.autolayout": True,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans"],
        "axes.titlesize": 12,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
    }
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import pandas as pd
import numpy as np
import folium
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def format_number(value):
    """Format numbers for better readability"""
    if isinstance(value, (int, float)):
        if isinstance(value, int):
            return f"{value:,}"
        return f"{value:,.2f}"
    return str(value)


def create_scatterplot(data, x_col, y_col, cluster_col, year):
    """Create a scatter plot"""
    try:
        logger.info(f"Creating scatterplot for year {year}")
        logger.info(f"Data shape: {data.shape}")
        logger.info(f"Columns available: {data.columns.tolist()}")

        # Validate input data
        if data.empty:
            logger.error("No data available for scatterplot")
            return None

        for col in [x_col, y_col, cluster_col]:
            if col not in data.columns:
                logger.error(f"Column {col} not found in data")
                return None

        # Clear any existing plots
        plt.close("all")

        # Create new figure using global settings
        plt.figure()

        # Create color palette
        unique_clusters = sorted(data[cluster_col].unique())
        n_clusters = len(unique_clusters)
        logger.info(f"Number of clusters: {n_clusters}")

        # Use seaborn's color palette
        cluster_palette = sns.color_palette("husl", n_colors=n_clusters)

        # Create scatterplot with improved styling
        scatter = sns.scatterplot(
            data=data,
            x=x_col,
            y=y_col,
            hue=cluster_col,
            hue_order=unique_clusters,
            palette=cluster_palette,
            s=100,  # Marker size
            alpha=0.7,  # Transparency
            edgecolor="white",  # Add white edge to points
            linewidth=0.5,
        )

        # Add labels and title with improved formatting
        plt.title(
            f'Scatter Plot of {x_col.replace("_", " ").title()} vs {y_col.replace("_", " ").title()} ({year})',
            pad=20,
            fontsize=12,
            fontweight="bold",
        )
        plt.xlabel(x_col.replace("_", " ").title(), fontsize=10, labelpad=10)
        plt.ylabel(y_col.replace("_", " ").title(), fontsize=10, labelpad=10)

        # Customize legend with improved styling
        legend = plt.legend(
            title="Cluster",
            title_fontsize=10,
            fontsize=9,
            bbox_to_anchor=(1.05, 1),
            loc="upper left",
            frameon=True,
            edgecolor="black",
        )
        legend.get_frame().set_alpha(0.9)

        # Add grid with improved styling
        plt.grid(True, linestyle="--", alpha=0.3, which="both")

        # Set axis limits with some padding
        x_min, x_max = data[x_col].min(), data[x_col].max()
        y_min, y_max = data[y_col].min(), data[y_col].max()
        x_padding = (x_max - x_min) * 0.05
        y_padding = (y_max - y_min) * 0.05
        plt.xlim(x_min - x_padding, x_max + x_padding)
        plt.ylim(y_min - y_padding, y_max + y_padding)

        # Improve layout
        plt.tight_layout()

        # Adjust layout before saving
        plt.tight_layout()

        # Save figure with high quality settings
        img_data = BytesIO()
        try:
            plt.savefig(
                img_data,
                format="png",
                dpi=300,
                bbox_inches="tight",
                facecolor="white",
                edgecolor="none",
                pad_inches=0.2,
                transparent=False,
                metadata={"Software": "Matplotlib"},
            )

            # Clean up
            plt.close("all")
            img_data.seek(0)

            # Create Image with specific size
            img = Image(img_data, width=7 * inch, height=5 * inch)
            logger.info("Successfully created and saved scatterplot")
            return img

        except Exception as save_error:
            logger.error(f"Error saving scatterplot: {str(save_error)}")
            logger.error("Traceback:", exc_info=True)
            return None
        finally:
            plt.close("all")  # Ensure cleanup even if save fails

    except Exception as e:
        logger.error(f"Error creating scatterplot: {str(e)}")
        logger.error("Traceback:", exc_info=True)
        logger.error(f"Data info: {data.info()}")
        return None


def create_boxplot(data, features, year):
    """Create a box plot for multiple features"""
    try:
        plt.figure(figsize=(12, 6))

        # Create box plot with improved styling
        box_plot = sns.boxplot(
            data=data[features],
            palette="Set3",
            linewidth=1,
            fliersize=5,
            showfliers=True,
        )

        # Add title and labels
        plt.title(
            f"Distribution of Features ({year})", pad=20, fontsize=12, fontweight="bold"
        )
        plt.xlabel("Features", fontsize=10)
        plt.ylabel("Value", fontsize=10)

        # Rotate and format x-axis labels
        plt.xticks(
            range(len(features)),
            [f.replace("_", " ").title() for f in features],
            rotation=45,
            ha="right",
        )

        # Format y-axis labels
        current_values = plt.gca().get_yticks()
        plt.gca().set_yticklabels([format_number(val) for val in current_values])

        # Add grid
        plt.grid(True, linestyle="--", alpha=0.7, axis="y")

        # Improve layout
        plt.tight_layout()

        img_data = BytesIO()
        plt.savefig(img_data, format="png", bbox_inches="tight", dpi=300)
        plt.close()
        img_data.seek(0)
        return Image(img_data, width=6 * inch, height=4 * inch)
    except Exception as e:
        logger.error(f"Error creating boxplot: {str(e)}")
        logger.error("Traceback:", exc_info=True)
        return None


def create_correlation_heatmap(data, features, year):
    """Create a correlation heatmap"""
    try:
        plt.figure(figsize=(10, 8))

        # Calculate correlations
        corr = data[features].corr()

        # Create mask for upper triangle
        mask = np.triu(np.ones_like(corr, dtype=bool))

        # Create heatmap with improved styling
        sns.heatmap(
            corr,
            mask=mask,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            vmin=-1,
            vmax=1,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
        )

        # Add title
        plt.title(
            f"Correlation Heatmap ({year})", pad=20, fontsize=12, fontweight="bold"
        )

        # Format axis labels
        feature_labels = [f.replace("_", " ").title() for f in features]
        plt.xticks(range(len(features)), feature_labels, rotation=45, ha="right")
        plt.yticks(range(len(features)), feature_labels, rotation=0)

        # Improve layout
        plt.tight_layout()

        img_data = BytesIO()
        plt.savefig(img_data, format="png", bbox_inches="tight", dpi=300)
        plt.close()
        img_data.seek(0)
        return Image(img_data, width=6 * inch, height=5 * inch)
    except Exception as e:
        logger.error(f"Error creating heatmap: {str(e)}")
        logger.error("Traceback:", exc_info=True)
        return None


def create_map_visualization(data, year):
    """Create a map visualization"""
    try:
        # Create base map centered on Indonesia
        m = folium.Map(location=[-2.5489, 118.0149], zoom_start=5)

        # Create color map
        n_clusters = len(data["cluster"].unique())
        colors = plt.cm.get_cmap("Set3")(np.linspace(0, 1, n_clusters))
        color_map = {
            i: f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
            for i, (r, g, b, _) in enumerate(colors)
        }

        # Add markers for each region
        for _, row in data.iterrows():
            if pd.notna(row.get("latitude")) and pd.notna(row.get("longitude")):
                # Create detailed popup content
                popup_content = f"""
                <div style="font-family: Arial, sans-serif;">
                    <h4 style="margin: 0 0 5px 0;">{row['kabupaten_kota']}</h4>
                    <p style="margin: 2px 0;">Cluster: {int(row['cluster'])}</p>
                    <p style="margin: 2px 0;">IPM: {format_number(row['ipm'])}</p>
                    <p style="margin: 2px 0;">Garis Kemiskinan: {format_number(row['garis_kemiskinan'])}</p>
                    <p style="margin: 2px 0;">Pengeluaran per Kapita: {format_number(row['pengeluaran_per_kapita'])}</p>
                </div>
                """

                # Add marker with improved styling
                folium.CircleMarker(
                    location=[float(row["latitude"]), float(row["longitude"])],
                    radius=8,
                    color=color_map.get(int(row["cluster"]), "#808080"),
                    popup=folium.Popup(popup_content, max_width=300),
                    fill=True,
                    fill_opacity=0.7,
                    weight=2,
                ).add_to(m)

        # Save map
        img_data = BytesIO()
        m.save(img_data, close_file=False)
        img_data.seek(0)
        return Image(img_data, width=7 * inch, height=5 * inch)
    except Exception as e:
        logger.error(f"Error creating map: {str(e)}")
        logger.error("Traceback:", exc_info=True)
        return None


def validate_data(data):
    """Validate clustering results data structure"""
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")

    if "yearly_results" not in data:
        raise ValueError("Missing 'yearly_results' in data")

    if not isinstance(data["yearly_results"], dict):
        raise ValueError("'yearly_results' must be a dictionary")

    if not data["yearly_results"]:
        raise ValueError("No year data found in 'yearly_results'")

    return True


def create_cluster_report_pdf(clustering_results, filename="cluster_report.pdf"):
    """
    Create a PDF report from clustering results with visualizations

    Args:
        clustering_results: Dictionary containing yearly clustering results
        filename: Name of the output PDF file

    Returns:
        BytesIO object containing the PDF
    """
    # Enable debugging for matplotlib
    logging.getLogger("matplotlib").setLevel(logging.DEBUG)
    logger.info(
        "Starting PDF generation with matplotlib backend: %s", matplotlib.get_backend()
    )

    # Log input data structure
    logger.info("Received clustering results structure:")
    logger.info(f"Keys in clustering_results: {clustering_results.keys()}")
    logger.info(f"Number of years: {len(clustering_results.get('yearly_results', {}))}")
    try:
        # Validate input data
        validate_data(clustering_results)

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        # Prepare styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
        )
        heading_style = ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading2"],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=24,
        )
        subheading_style = ParagraphStyle(
            "CustomSubHeading",
            parent=styles["Heading3"],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=16,
        )
        normal_style = styles["Normal"]

        # Build document content
        content = []

        # Title
        content.append(Paragraph("Clustering Analysis Report", title_style))
        content.append(Spacer(1, 20))

        # Algorithm Information
        algorithm_name = clustering_results.get("algorithm", "Unknown")
        content.append(Paragraph(f"Algorithm: {algorithm_name}", heading_style))

        # Process each year's results
        yearly_results = clustering_results.get("yearly_results", {})

        for year, year_data in yearly_results.items():
            try:
                logger.info(f"Processing year {year}")

                content.append(PageBreak())
                content.append(Paragraph(f"Analysis for Year {year}", heading_style))

                # Evaluation Metrics
                content.append(Paragraph("Evaluation Metrics", subheading_style))
                evaluation = year_data.get("evaluation", {})
                eval_data = [
                    ["Metric", "Score"],
                    [
                        "Davies-Bouldin Index",
                        format_number(evaluation.get("davies_bouldin")),
                    ],
                    [
                        "Silhouette Score",
                        format_number(evaluation.get("silhouette_score")),
                    ],
                ]

                eval_table = Table(eval_data, colWidths=[200, 300])
                eval_table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("FONTSIZE", (0, 0), (-1, 0), 12),
                            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                            ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                            ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ]
                    )
                )
                content.append(eval_table)
                content.append(Spacer(1, 20))

                # Process data for visualizations
                if year_data.get("data"):
                    df = pd.DataFrame(year_data["data"])
                    if not df.empty:
                        # Visualizations section
                        content.append(
                            Paragraph("Data Visualizations", subheading_style)
                        )

                        # Add scatterplot
                        plot = create_scatterplot(
                            df, "ipm", "pengeluaran_per_kapita", "cluster", year
                        )
                        if plot:
                            content.append(plot)
                            content.append(Spacer(1, 10))

                        # Add boxplot
                        features = ["ipm", "garis_kemiskinan", "pengeluaran_per_kapita"]
                        plot = create_boxplot(df, features, year)
                        if plot:
                            content.append(plot)
                            content.append(Spacer(1, 10))

                        # Add correlation heatmap
                        plot = create_correlation_heatmap(df, features, year)
                        if plot:
                            content.append(plot)
                            content.append(Spacer(1, 10))

                        # Add map visualization
                        if "latitude" in df.columns and "longitude" in df.columns:
                            plot = create_map_visualization(df, year)
                            if plot:
                                content.append(plot)
                                content.append(Spacer(1, 20))

                # Cluster Details
                clusters = year_data.get("clusters", [])
                if clusters:
                    content.append(Paragraph("Cluster Details", subheading_style))

                    for cluster in clusters:
                        cluster_id = cluster.get("id")
                        size = cluster.get("size", 0)
                        content.append(
                            Paragraph(
                                f"Cluster {cluster_id} (Size: {size})", subheading_style
                            )
                        )

                        # Member information with memberships
                        members = cluster.get("members", [])
                        if members:
                            member_data = [
                                [
                                    "Region",
                                    "IPM",
                                    "Garis Kemiskinan",
                                    "Pengeluaran per Kapita",
                                    "Membership",
                                ]
                            ]
                            for member in members:
                                member_data.append(
                                    [
                                        member.get("kabupaten_kota", ""),
                                        format_number(member.get("ipm", 0)),
                                        format_number(
                                            member.get("garis_kemiskinan", 0)
                                        ),
                                        format_number(
                                            member.get("pengeluaran_per_kapita", 0)
                                        ),
                                        format_number(member.get("membership", 0)),
                                    ]
                                )

                            member_table = Table(
                                member_data, colWidths=[120, 80, 100, 120, 80]
                            )
                            member_table.setStyle(
                                TableStyle(
                                    [
                                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                                        (
                                            "TEXTCOLOR",
                                            (0, 0),
                                            (-1, 0),
                                            colors.whitesmoke,
                                        ),
                                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                                        ("FONTSIZE", (0, 0), (-1, -1), 8),
                                    ]
                                )
                            )
                            content.append(member_table)
                            content.append(Spacer(1, 10))
            except Exception as e:
                logger.error(f"Error processing year {year}: {str(e)}")
                logger.error(traceback.format_exc())
                continue

        # Build PDF
        doc.build(content)
        buffer.seek(0)
        return buffer
    except Exception as e:
        logger.error("Error creating PDF report:")
        logger.error(traceback.format_exc())
        raise


def generate_cluster_report(clustering_results):
    """
    Generate a PDF report for clustering results

    Args:
        clustering_results: Dictionary containing clustering results

    Returns:
        BytesIO object containing the PDF
    """
    try:
        return create_cluster_report_pdf(clustering_results)
    except Exception as e:
        logger.error("Error in generate_cluster_report:")
        logger.error(traceback.format_exc())
        raise
